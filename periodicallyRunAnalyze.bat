@echo off

@echo Periodically Run Analyze Space

:analyze

start .\venv\Scripts\python.exe analyzeSpaces_MultiCore.py
@rem run analyzeSpaces_MultiCore in another window

TIMEOUT /T 99999 /nobreak
@rem 84600 sec = 1 day

cls
@rem clear history

goto analyze
@rem infinite loop