#Requires AutoHotkey v2.0

;--------------------------------------------------
; Emergency stop
;--------------------------------------------------

Esc:: {
    ExitApp()
}

;--------------------------------------------------
; Main automation loop
;--------------------------------------------------

Loop {

    ;----------------------------------------------
    ; Startup Delay
    ;----------------------------------------------

    Sleep(8000)


    ;----------------------------------------------
    ; Phase 1: Input Item Category
    ;----------------------------------------------

    Send("{Home}")
    Sleep(Random(400, 700))

    Send("+{End}")
    Sleep(Random(400, 700))

    Send("^c")
    Sleep(Random(400, 700))

    ; Check if the text just copied is the termination signal
    if InStr(A_Clipboard, "END_OF_SCRIPT") {
        ExitApp()
    }

    Send("^{Left}")
    Sleep(Random(700, 900))

    Send("{Home}")
    Sleep(Random(700, 900))

    Send("{Down}")
    Sleep(Random(700, 900))


    ; Switch from text editor -> trade tab
    Send("^{Tab}")
    Sleep(Random(400, 700))

    ; Reverse-tab to top of page
    Loop 50 {
        Send("+{Tab}")
        Sleep(Random(150, 250))
    }

    Loop 2 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Send("{Down}")
    Sleep(Random(700, 900))

    Send("{Enter}")
    Sleep(Random(700, 900))

    Loop 2 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Send("^v")
    Sleep(Random(400, 700))

    Send("{Enter}")
    Sleep(Random(400, 700))


    Loop 2 {
        Send("+{Tab}")
        Sleep(Random(400, 700))
    }

    Loop 13 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }


    ; Switch trade -> text editor
    Send("^{Tab}")
    Sleep(Random(400, 700))


    ;----------------------------------------------
    ; Phase 2: Input item modifier
    ;----------------------------------------------

    Send("+{End}")
    Sleep(Random(700, 900))

    Send("^c")
    Sleep(Random(700, 900))

    Send("^{Left}")
    Sleep(Random(700, 900))

    Send("{Home}")
    Sleep(Random(700, 900))

    Send("{Down}")
    Sleep(Random(700, 900))


    ; Switch text editor -> trade
    Send("^{Tab}")
    Sleep(Random(400, 700))


    Loop 3 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Send("^v")
    Sleep(Random(400, 700))

    Send("{Enter}")
    Sleep(Random(400, 700))


    Loop 1 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Loop 3 {
        Send("+{Tab}")
        Sleep(Random(400, 700))
    }


    ; Switch trade -> text editor
    Send("^{Tab}")
    Sleep(Random(400, 700))


    ;----------------------------------------------
    ; Phase 3: Input minimum value
    ;----------------------------------------------

    Send("+{End}")
    Sleep(Random(700, 900))

    Send("^c")
    Sleep(Random(700, 900))

    Send("^{Left}")
    Sleep(Random(700, 900))

    Send("{Home}")
    Sleep(Random(700, 900))

    Send("{Down}")
    Sleep(Random(700, 900))


    ; Switch text editor -> trade
    Send("^{Tab}")
    Sleep(Random(400, 700))


    Send("^v")
    Sleep(Random(400, 700))


    Loop 3 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Send("+3")
    Sleep(Random(400, 700))

    Send("{Space}")
    Sleep(Random(400, 700))

    Send("m")
    Sleep(Random(400, 700))

    Send("{Enter}")
    Sleep(Random(400, 700))


    Loop 4 {
        Send("+{Tab}")
        Sleep(Random(400, 700))
    }

    Send("1")
    Sleep(Random(400, 700))

    Send("{Tab}")
    Sleep(Random(400, 700))

    Send("1")
    Sleep(Random(400, 700))

    ; Verify that both fields actually contain "1".
    ; If not, terminate the script.

    Send("^a")
    Sleep(Random(400, 700))

    Send("^c")
    Sleep(Random(400, 700))

    ClipWait(1)

    if Trim(A_Clipboard) != "1" {
        MsgBox("Verification failed. Expected '1' but found:`n`n" A_Clipboard)
        ExitApp()
    }

    ;----------------------------------------------
    ; Phase 4: Search and copy results back
    ;----------------------------------------------

    Loop 5 {
        Send("{Tab}")
        Sleep(Random(400, 700))
    }

    Send("{Enter}")
    Sleep(Random(8000, 11000))

    ; Scroll to bottom of top 100 search results
    Loop 15 {
        Send("{PgDn}")
        Sleep(Random(1400, 1700))
    }

    Sleep(Random(400, 700))

    Send("^a")
    Sleep(Random(400, 700))

    Send("^c")
    Sleep(Random(400, 700))


    ; Switch trade -> text editor
    Send("^{Tab}")
    Sleep(Random(400, 700))

    Send("^v")
    Sleep(Random(400, 700))

    Send("{Enter}")
    Sleep(Random(400, 700))


    ;----------------------------------------------
    ; Phase 5: Save the url for later
    ;----------------------------------------------

    ; Switch text editor -> trade
    Send("^{Tab}")
    Sleep(Random(400, 700))

    Send("^l")
    Sleep(Random(400, 700))

    Send("^c")
    Sleep(Random(400, 700))

    ; Switch trade -> text editor
    Send("^{Tab}")
    Sleep(Random(700, 900))

    Send("^v")
    Sleep(Random(700, 900))

    Send("{Enter}")
    Sleep(Random(700, 900))

    Send("{Enter}")
    Sleep(Random(700, 900))

    Send("{Down}")
    Sleep(Random(700, 900))


    ;----------------------------------------------
    ; Phase 6: Reset for next loop
    ;----------------------------------------------

    ; Switch text editor -> trade
    Send("^{Tab}")
    Sleep(Random(400, 700))

    Send("^l")
    Sleep(Random(400, 700))

    ; Tab to reset button
    Loop 40 {
        Send("{Tab}")
        Sleep(Random(150, 250))
    }

    Send("^l")
    Sleep(Random(400, 700))

    Loop 9 {
        Send("+{Tab}")
        Sleep(Random(150, 250))
    }

    Send("{Enter}")
    Sleep(Random(400, 700))

    Send("^l")
    Sleep(Random(400, 700))

    ; Tab to return to search button
    Loop 18 {
        Send("{Tab}")
        Sleep(Random(150, 250))
    }

    Send("{Enter}")
    Sleep(Random(400, 700))

    ; Return to text editor before next iteration
    Send("^{Tab}")
    Sleep(Random(400, 700))
}