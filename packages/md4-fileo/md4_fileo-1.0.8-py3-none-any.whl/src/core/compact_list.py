from loguru import logger

from PyQt6.QtCore import Qt, QUrl, QRect, pyqtSignal, pyqtSlot, QPoint
from PyQt6.QtGui import (QGuiApplication, QKeySequence, QShortcut,
)
from PyQt6.QtWidgets import (QTextBrowser, QWidget, QVBoxLayout,
    QMenu, QLineEdit, QApplication,
)

from . import app_globals as ag


class editTag(QWidget):
    def __init__(self, text: str, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("editTag")
        self.editor = QLineEdit(self)
        self.editor.setObjectName("editor")
        self.editor.setText(text)
        self.editor.setFocus(Qt.FocusReason.OtherFocusReason)
        self.editor.setCursor(Qt.CursorShape.ArrowCursor)
        self.editor.selectAll()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.editor)
        self.setLayout(layout)

        self.adjustSize()
        self.editor.editingFinished.connect(self.finish_edit)

        escape = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        escape.activated.connect(self.cancel)

    @pyqtSlot()
    def finish_edit(self):
        txt = self.editor.text()
        self.parent().edit_item.emit(txt)
        self.parent().browser.setFocus()
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.parent().browser.setFocus()
        self.close()

class aBrowser(QWidget):
    edit_item = pyqtSignal(str)
    delete_items = pyqtSignal(str)
    change_selection = pyqtSignal(list)
    edit_finished = pyqtSignal()

    def __init__(self, brackets: bool=False,
        read_only: bool=True, parent=None) -> None:
        super().__init__(parent)
        self.read_only = read_only
        self.brackets = brackets

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.browser: QTextBrowser = QTextBrowser()
        self.browser.setObjectName('a_browser')
        self.browser.selectionChanged.connect(self.selection_changed)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.browser.customContextMenuRequested.connect(self.custom_menu)
        self.browser.setOpenLinks(False)

        self.tags = []
        self.tag_ids = []
        self.selected_idx = []
        self.curr_pos = 0
        self.scroll_pos = 0

        self.browser.anchorClicked.connect(self.ref_clicked)

        if not self.read_only:
            f2 = QShortcut(QKeySequence(Qt.Key.Key_F2), self.browser)
            f2.setContext(Qt.ShortcutContext.WidgetShortcut)
            f2.activated.connect(self.rename_tag)

    @pyqtSlot()
    def rename_tag(self):
        """
        edit last selected tag - current tag
        """
        if not self.selected_idx:
            return
        c_rect = self.get_edit_rect()
        if c_rect:
            ed = editTag(self.get_current(), self)
            ed.setGeometry(c_rect)
            ed.show()

    def get_edit_rect(self):
        start, end = self.get_start_end()

        if start.y() < end.y():   # two line selection
            w = self.browser.width()
            return QRect(
                4, end.y()+end.height(),
                w-start.x()+end.x(), end.height()
            )

        return QRect(
            start.x()+4,
            end.y()+end.height(),
            end.x()-start.x()+12,
            end.height()
        )

    def get_start_end(self):
        curs = self.browser.textCursor()

        # curs.setPosition(pos)
        end = self.browser.cursorRect(curs)

        pos = curs.position()
        tag = self.get_current()
        curs.setPosition(pos - len(tag))
        start = self.browser.cursorRect(curs)
        return start, end

    @pyqtSlot(QPoint)
    def custom_menu(self, pos):
        self.scroll_pos = self.browser.verticalScrollBar().value()
        menu = QMenu(self)
        if not self.read_only:
            menu.addAction("Delete selected")
            menu.addAction("Edit current")
        menu.addAction("Copy selected")
        menu.addSeparator()
        menu.addAction("Select all")
        action = menu.exec(self.browser.mapToGlobal(pos))
        if action:
            {"Delete selected": self.delete_selected,
             "Edit current": self.rename_tag,
             "Copy selected": self.copy_selected,
             "Select all": self.select_all,
             }[action.text()]()

    def delete_selected(self):
        if not self.selected_idx:
            return
        ids = ','.join((str(id) for id in self.get_selected_ids()))
        self.delete_items.emit(ids)

    def copy_selected(self):
        tags = self.get_selected()
        QApplication.clipboard().setText(';'.join(tags))

    def set_list(self, items: list):
        self.tags.clear()
        self.tag_ids.clear()
        self.selected_idx.clear()
        for it in items:
            self.tags.append(it[0])
            self.tag_ids.append(it[1])
        self.show_in_bpowser()

    @pyqtSlot()
    def selection_changed(self):
        """
        I need not to show selection as text, but selection as keywords,
        so the selection is cleared whenever the user tries to do so;
        selection is doing in self.ref_clicked() method
        """
        curs = self.browser.textCursor()
        if curs.hasSelection():
            curs.clearSelection()
            self.browser.setTextCursor(curs)

    def set_selection(self, sel_ids: list[int]):
        if len(self.tags) > 0:
            self.selected_idx = [self.tag_ids.index(int(s)) for s in sel_ids]
            self.show_in_bpowser()
            self.browser.find(self.get_current())

    def change_selection_emit(self):
        items = [val for i,val in enumerate(self.tags) if i in self.selected_idx]
        self.change_selection.emit(items)

    def select_all(self):
        self.selected_idx = list(range(len(self.tag_ids)))
        self.show_in_bpowser()

    def get_selected_ids(self) -> list[int]:
        tmp = [self.tag_ids[i] for i in self.selected_idx]
        tmp.sort()
        return tmp

    def get_tag_id(self, tag: str) -> bool:
        try:
            return self.tag_ids[self.tags.index(tag)]
        except ValueError:
            return 0

    @pyqtSlot(QUrl)
    def ref_clicked(self, href: QUrl):
        self.scroll_pos = self.browser.verticalScrollBar().value()
        mod = QGuiApplication.keyboardModifiers()
        self.update_selected(href, mod)
        self.change_selection_emit()
        self.show_in_bpowser()

    def get_selected(self) -> list[str]:
        tmp = [self.tags[i] for i in self.selected_idx]
        tmp.sort(key=str.lower)
        return tmp

    def get_current(self) -> str:
        """
        the current tag is the last selected tag
        that is the last one in self.selected_idx
        """
        return self.tags[self.selected_idx[-1]] if self.selected_idx else ''

    def current_id(self) -> int:
        return self.tag_ids[self.selected_idx[-1]] if self.selected_idx else 0

    def update_selected(self, href: QUrl, mod: Qt.KeyboardModifier):
        tref = href.toString()[1:]
        self.curr_pos = self.browser.textCursor().position()
        if tref not in self.tags:
            # no new tags created in this module
            # so this shouldn't happen
            return
        self.browser.find(tref)
        i = self.tags.index(tref)
        if mod is Qt.KeyboardModifier.ControlModifier:
            if i in self.selected_idx:
                self.selected_idx.remove(i)
            else:
                self.selected_idx.append(i)
        else:
            if self.selected_idx == [i]:
                self.selected_idx.clear()
                return
            self.selected_idx.clear()
            self.selected_idx.append(i)

    def show_in_bpowser(self):
        self.browser.clear()
        style = ag.dyn_qss['text_browser'][0]
        inn = self.html_selected()
        self.browser.setText(''.join((style, inn)))
        curs = self.browser.textCursor()
        curs.setPosition(self.curr_pos)
        self.browser.setTextCursor(curs)
        self.browser.verticalScrollBar().setValue(self.scroll_pos)

    def html_selected(self):
        sel = self.selected_idx
        if self.brackets:
            if sel:
                return ' '.join(f"<a class={'c' if i == sel[-1] else 's' if i in sel else 't'}"
                    f' href="#{tag}">[{tag}]</a> ' for i,tag in enumerate(self.tags))
            return ' '.join(f'<a class t href="#{tag}">[{tag}]</a> ' for tag in self.tags)
        if sel:
            return ' '.join(f"<a class={'c' if i == sel[-1] else 's' if i in sel else 't'}"
                f' href="#{tag}">{tag}</a> ' for i,tag in enumerate(self.tags))
        return ' '.join(f'<a class t href="#{tag}">{tag}</a> ' for tag in self.tags)
