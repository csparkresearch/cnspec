PYUIC?=pyuic5
PYRCC?=pyrcc5
PY_VERSION ?= 2

UI_FILES = $(shell ls *.ui)
RC_FILES = $(shell ls *.qrc)

UI_COMPILED = $(patsubst %.ui, ui_%.py, $(UI_FILES))
RC_COMPILED = $(patsubst %.qrc, %_rc.py, $(RC_FILES))

ifeq ($(PY_VERSION),3)
	ifneq (,$(findstring pyrcc4,$(PYRCC)))
		override PYRCC += -py3
	endif
endif
$(info PYRCC=$(PYRCC))

 
all: $(UI_COMPILED) $(RC_COMPILED)

clean:
	rm -f $(UI_COMPILED) $(RC_COMPILED)
	rm -rf *.pyc *~ __pycache__

ui_%.py:  %.ui
	$(PYUIC) --from-import $< -o $@


%_rc.py: %.qrc
	$(PYRCC) $< -o $@

.PHONY: all clean
