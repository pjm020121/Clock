'''
Program name
- Clock

Library
- tkinter
- re
- datetime

Class
- Clock

Method
- init
- Real_time
- Update_time
- Clock_on_resize
- Timer
- Start_timer
- Update_clock
- Key_del_press
- Exit
- Timer_on_resize
- Stop_timer
- unbind_space_event
- bind_space_event
- Reverse_function

Event
- Configure
- Escape
- Button-3
- Key(delete)
- space
- Return

Function
- 이 프로그램은 현재 시각과 타이머 기능을 보유한 프로그램이다.
  프로세스는 항상 전면에 고정되어 있으며 default로 현재시각이 setting되어 있다.
  font size는 프로세스의 크기에 비례하여 조절된다.
  Button-3(마우스 오른쪽 버튼)로 현 시각과 타이머를 상시변경가능하다.
  esc키를 이용해 프로세스를 종료시킬 수 있다.


- REAL_TIME
    - 현 시각을 표시한다.

- TIMER
    - 타이머 기능을 제공하며 자리수는 각 자리에서 두자리수까지 입력가능하다.
    - 시간 입력 후 enter키를 통하여 타이머를 실행가능하며 space키를 이용해 정지 및 재실행이 가능하다.
    - Key(delete)를 통하여 setting time을 format가능하다.
'''

import tkinter
import re
from tkinter import messagebox
from datetime import datetime

class Clock:

    def __init__(self):

        # instance default structure
        self.module = tkinter.Tk()
        self.module.geometry("500x200+100+100")
        self.reverse_stack = True
        self.timestack = True
        self.running = False

        # static process(front)
        self.module.attributes("-topmost", True)

        # event
        self.module.bind("<Escape>", self.Exit)

        # method call
        self.Real_time()

    # real_time object
    def Real_time(self):

        # real_time default structure
        self.module.title("Clock")
        self.label = tkinter.Label(self.module, font=("Helvetica", 48), bg='white')
        self.label.pack(expand=True, fill='both')

        # event
        self.module.bind("<Configure>", self.Clock_on_resize)
        self.module.bind("<Button-3>", self.Reverse_function)

        # method call
        self.Update_time()

        # object mainloop
        self.module.mainloop()

    # insert real_time
    def Update_time(self):
        time = datetime.now()
        real_time = time.strftime("%H:%M:%S")
        self.label.config(text=real_time)
        self.label.after(1000, self.Update_time)

    # size normalization
    def Clock_on_resize(self, event):
        new_font_size = int(event.width / 5.5)
        updated_font = ('Helvetica', new_font_size)
        self.label.config(font=updated_font)

    # timer object
    def Timer(self):

        # Timer default structure
        self.module.title("Timer")
        self.entry = tkinter.Entry(self.module, font=("Helvetica", 48), justify="center", insertbackground="black")
        self.entry.pack(expand=True, fill='both')
        self.entry.insert(0, "00:00:00")

        # event
        self.module.bind("<Configure>", self.Timer_on_resize)
        self.module.bind("<Key>", self.Key_del_press)
        self.module.bind("<Button-3>", self.Reverse_function)
        self.module.bind("<space>", self.Stop_timer)
        self.entry.bind("<Return>", self.Start_timer)

        # object mainloop
        self.module.mainloop()

    # timer start
    def Start_timer(self, event):

        # running이 false이거나 timestack이 true일때만 이벤트 실행
        if self.running is not True and self.timestack is True:

            self.entry.config(insertbackground="black")
            entered_time = self.entry.get()

            try:
                # 입력된 시간의 형식을 확인
                if not re.match(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}$', entered_time):
                    raise ValueError("잘못 입력하셨습니다.\n다시입력해주세요.")

                # 엔트리 문자열 정수로 매핑
                hours, minutes, seconds = map(int, entered_time.split(":"))
                total_seconds = hours * 3600 + minutes * 60 + seconds

                self.remaining_time = total_seconds
                self.running = True
                self.Update_clock()

            except ValueError as e:
                tkinter.messagebox.showerror("Error 발생", str(e))

                # 입력값이 유효하지 않은 경우 초기값으로 돌아감
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, "00:00:00")

    # timer update
    def Update_clock(self):

        # running상태 확인
        if hasattr(self, 'running') and self.running and self.remaining_time >= 0:
            self.entry.config(insertbackground="white")
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

            # entry남은 시간 확인
            if self.remaining_time == 0:
                self.running = False
                self.entry.config(fg="red")
                self.module.after(2000, lambda: self.entry.config(fg='black', insertbackground="black"))
            else:
                self.entry.config(fg="black")

            # 시간 업데이트
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.time_str)
            self.remaining_time -= 1
            self.update_clock_id = self.module.after(1000, self.Update_clock)

    # reset
    def Key_del_press(self, event):

        # event key 'Del'
        if event.keysym == 'Delete':
            self.running = False
            self.entry.config(insertbackground='black')
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, "00:00:00")

    # exit
    def Exit(self, event):
        result = messagebox.askyesno("종료", "프로그램을 종료하시겠습니까?")
        if result:
            self.module.destroy()

    # font size update
    def Timer_on_resize(self, event):
        new_font_size = int(event.width / 5.5)
        updated_font = ('Helvetica', new_font_size)
        self.entry.config(font=updated_font)

    # timer stop & restart
    def Stop_timer(self, event):

        self.unbind_space_event()

        if self.timestack:
            self.running = False
            self.timestack = False
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.time_str)

        else:
            self.running = True
            self.timestack = True
            self.Update_clock()

    # 스페이스 바 이벤트 1초동안 비활성화
    def unbind_space_event(self):
        self.module.unbind("<space>")
        self.module.after(1000, self.bind_space_event)

    # 스페이스 바 이벤트 다시 활성화
    def bind_space_event(self, event=None):
        self.module.bind("<space>", self.Stop_timer)

    # function change
    def Reverse_function(self, event):

        # turn to timer
        if self.reverse_stack:
            self.label.destroy()
            self.reverse_stack = False
            self.Timer()

        # turn to real_time
        else:
            self.running = False
            self.entry.destroy()
            self.reverse_stack = True
            self.Real_time()

if __name__ == "__main__":
    # CLOCK object generate
    Clock_application = Clock()

