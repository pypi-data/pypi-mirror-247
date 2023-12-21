# ltermio - Lightweight POSIX terminal I/O library

The package contains four modules: **cursor**, **termkey**, **color256** and **unicon**. Tested only on **MacOS terminal** and **iTerm2**, so the platform compatibility has not been well verfied yet.
All functions are based on **CSI** sequences and **termios**, no additional requirements other than the standard library.

## cursor
Wrapper functions of **CSI(Control Sequence Introducer)** sequences about cursor and screen. And additionally provides a several of functions for text composing.

## termkey
Just two functions **getch()** and **getkey()** for reading keyboard in non-canonical mode.  **getch()** reads raw key characters byte by byte, **getkey()** calls getch() and transforms the CSI sequences of function keys into key codes that defined in an enumerate class Key.

## color256
Sets 256-color display attributes of the character terminal.

## unicon
Collection of some common icons in unicode character set.
