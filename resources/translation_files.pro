TEMPLATE = app
TARGET = ts
INCLUDEPATH += mounzil


# Input
SOURCES +=  ../mounzil/gui/about_ui.py \
            ../mounzil/gui/addlink_ui.py \
            ../mounzil/gui/after_download_ui.py \
            ../mounzil/gui/log_window_ui.py \
            ../mounzil/gui/mainwindow_ui.py \
            ../mounzil/gui/progress_ui.py \
            ../mounzil/gui/setting_ui.py \
            ../mounzil/gui/text_queue_ui.py \
	    ../mounzil/scripts/after_download.py \
        ../mounzil/scripts/mainwindow.py \
	    ../mounzil/scripts/progress.py \
	    ../mounzil/scripts/update.py \
        ../mounzil/scripts/setting.py \
			../mounzil/scripts/video_finder_addlink.py
TRANSLATIONS += locales/ui.ts

