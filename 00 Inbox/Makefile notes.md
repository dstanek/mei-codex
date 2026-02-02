Here's a table of the different assignment operators available in Makefiles:

|Operator|Name|Description|
|---|---|---|
|`=`|Recursive/Lazy Assignment|Value is expanded when the variable is used, not when it's defined. Allows forward references and recursive definitions.|
|`:=`|Simple/Immediate Assignment|Value is expanded immediately when the variable is defined. Similar to assignment in most programming languages.|
|`::=`|Simple Assignment (POSIX)|Same as `:=` but follows POSIX standard. Available in newer versions of Make.|
|`?=`|Conditional Assignment|Sets the variable only if it's not already defined or is empty. Useful for providing default values.|
|`+=`|Append Assignment|Appends the value to the existing variable value, separated by a space. Uses the same expansion rules as the original assignment.|
|`!=`|Shell Assignment|Executes the right-hand side as a shell command and assigns the output to the variable.|

**Examples:**

```Makefile
# Recursive assignment - FOO is expanded when BAR is used
FOO = $(BAR)
BAR = Hello World
# BAR will contain "Hello World"

# Immediate assignment - expanded right away
FOO := $(shell date)
# FOO contains the current date/time when this line is processed

# Conditional assignment
CC ?= gcc
# Sets CC to gcc only if CC wasn't already defined

# Append assignment
CFLAGS = -Wall
CFLAGS += -g -O2
# CFLAGS now contains "-Wall -g -O2"

# Shell assignment
DATE != date
# DATE contains the output of the date command
```