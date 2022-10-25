from fractions import Fraction
from string import ascii_lowercase
from typing import List, Optional, Callable, Dict

from sympy import Matrix, linsolve, FiniteSet
import tkinter as tk

MAX_VARS = len(ascii_lowercase)

ComplainCB = Callable[[str, Optional[str]], None]








class UICell:
    def __init__(
            self, parent: tk.Widget, complain: ComplainCB, row: int, col: int,
            justify: str = tk.LEFT,
    ) -> None:
        self.complain = complain
        self.var_name = f'cell_{row}_{col}'

        # not DoubleVar - it needs to be Fraction-parseable
        self.var = tk.StringVar(
            master=parent,
            name=self.var_name,
            value='0',
        )
        self.trace_id = self.var.trace_add('write', self.changed)
        self.entry = tk.Entry(
            master=parent,
            textvariable=self.var,
            width=6,
            justify=justify,
        )
        self.entry.grid(row=row, column=col)
        self.value: Optional[Fraction] = Fraction(0)

    def destroy(self) -> None:
        self.var.trace_remove('write', self.trace_id)
        self.entry.destroy()

    def changed(self, name: str, index: str, mode: str) -> None:
        try:
            self.value = Fraction(self.var.get())
        except ValueError:
            self.value = None

        if self.value is None:
            complaint = 'Invalid number'
            colour = '#FCD0D0'
        else:
            complaint = None
            colour = 'white'
        self.entry.configure(background=colour)
        self.complain(self.var_name, complaint)


class UIVarCell(UICell):
    def __init__(self, parent: tk.Widget, complain: ComplainCB, row: int, col: int, letter: str) -> None:
        super().__init__(parent, complain, row, col, tk.RIGHT)
        self.letter = letter
        self.separator = tk.Label(master=parent)
        self.separator.grid(sticky=tk.W, row=row, column=1 + col)

    def destroy(self) -> None:
        super().destroy()
        self.separator.destroy()

    def set_separator(self, rightmost: bool) -> None:
        if rightmost:
            sep = '='
        else:
            sep = '+'
        self.separator.config(text=f'{self.letter} {sep}')


class UIVariable:
    def __init__(self, parent: tk.Widget, complain: ComplainCB, index: int) -> None:
        self.parent, self.complain, self.index = parent, complain, index
        self.letter = ascii_lowercase[index]
        self.cells: List[UIVarCell] = []

        self.result_var = tk.StringVar(
            master=parent,
            value='',
            name=f'result_{index}',
        )
        self.result_entry = tk.Entry(
            master=parent,
            state='readonly',
            textvariable=self.result_var,
            width=6,
            justify=tk.RIGHT,
        )
        self.result_label = tk.Label(master=parent, text=f'={self.letter}')
        self.result_entry.grid(sticky=tk.E, row=1 + MAX_VARS, column=2 * index)
        self.result_label.grid(sticky=tk.W, row=1 + MAX_VARS, column=2 * index + 1)

        for _ in range(index + 1):
            self.grow()

    def grow(self) -> None:
        self.cells.append(UIVarCell(
            parent=self.parent,
            complain=self.complain,
            row=1 + len(self.cells),
            col=2 * self.index,
            letter=self.letter,
        ))

    def shrink(self) -> None:
        self.cells.pop().destroy()

    def destroy(self) -> None:
        for widget in (self.result_label, self.result_entry):
            widget.destroy()
        while self.cells:
            self.shrink()

    def set_result(self, s: str) -> None:
        self.result_var.set(s)


class UIFrame:
    def __init__(self, parent: tk.Tk):
        # parent.clipboard_get()
        parent.winfo_server()
        self.root = root = tk.Frame(master=parent, bg='blue', height=500, width=500)

        self.variables: List[UIVariable] = []
        self.sums: List[UICell] = []
        self.complaints: Dict[str, str] = {}

        parent.geometry('500x800')
        self.count = tk.IntVar(master=root, name='count', value=2)
        self.count.trace_add('write', self.count_changed)

        def walk_through():
            frame = tk.Frame(bg='green', bd=0.5)
            frame.place(relheight=0.5, relx=0.25, relwidth=0.5, rely=0.35)

            image = tk.PhotoImage(file='logo1.png')
            label = tk.Label(frame, image=image)
            label.pack()

        tk.Button(master=parent, text='show walk through', bg='pink', command=walk_through())

        tk.Label(
            master=root, text='How many  Variables'
        ).grid(row=0, column=0, sticky=tk.E)
        tk.Spinbox(
            master=root,
            from_=2,
            to=MAX_VARS,
            increment=1,
            width=4,  # characters
            textvariable=self.count,  # triggers a first call to count_changed
        ).grid(row=0, column=1, columnspan=2, sticky=tk.W)

        self.error_label = tk.Label(master=root, text='', foreground='red')
        # Row indices do not need to be contiguous, so choose one that will
        # always be at the bottom - one for the spinbox, max vars, and one for
        # the result row.
        self.error_label.grid(row=1 + MAX_VARS + 1, column=0, columnspan=MAX_VARS + 1)

        root.pack()

    def count_changed(self, name: str, index: str, mode: str) -> None:
        try:
            requested = self.count.get()
        except tk.TclError:
            return

        if 2 <= requested <= MAX_VARS:
            for var in self.variables:
                var.set_result('')
            while len(self.variables) < requested:
                self.grow()
            while len(self.variables) > requested:
                self.shrink()

    def grow(self) -> None:
        for var in self.variables:
            var.grow()
            for cell in var.cells:
                cell.set_separator(rightmost=False)

        var = UIVariable(
            parent=self.root, complain=self.complain,
            index=len(self.variables),
        )
        for cell in var.cells:
            cell.set_separator(rightmost=True)
        self.variables.append(var)

        self.sums.append(UICell(
            parent=self.root, complain=self.complain,
            row=1 + len(self.sums), col=2 * MAX_VARS,
        ))

    def shrink(self) -> None:
        self.sums.pop().destroy()
        self.variables.pop().destroy()
        for var in self.variables:
            var.shrink()
        for cell in self.variables[-1].cells:
            cell.set_separator(rightmost=True)

    def complain(self, var_name: str, complaint: Optional[str]) -> None:
        if complaint is None:
            self.complaints.pop(var_name, None)
        else:
            self.complaints[var_name] = complaint
        self.error_text = ', '.join(self.complaints.values())

        if not self.complaints:
            self.solve()

    @property
    def error_text(self) -> str:
        return self.error_label.cget('text')

    @error_text.setter
    def error_text(self, s: str) -> None:
        self.error_label.configure(text=s)

    @property
    def matrix(self) -> Matrix:
        return Matrix([
            [c.value for c in var.cells]
            for var in self.variables
        ]).T

    @property
    def sum_vector(self) -> Matrix:
        return Matrix([c.value for c in self.sums])

    def solve(self) -> None:
        res_set = linsolve((self.matrix, self.sum_vector))
        if not isinstance(res_set, FiniteSet):
            self.error_text = 'No finite set of solutions'
        elif len(res_set) < 1:
            self.error_text = 'No solution found'
        elif len(res_set) > 1:
            self.error_text = 'Non-unique solution space'
        else:
            self.error_text = ''
            result, = res_set
            for var, res in zip(self.variables, result):
                var.set_result(res)
            return

        for var in self.variables:
            var.set_result('')




def main() -> None:
    parent = tk.Tk()
    parent.title('Simultaneous linear equation solver')
    UIFrame(parent)
    parent.mainloop()


main()
