# AQA Assembly


```Python
import xai16

xai16.emulate('''
start:  MOV R0, #5
        MOV R1, #6
        ADD R2, R0, R1
        HALT
''')
```

## Instructions

    B   address
    BEQ address
    BNE address
    BGT address
    BLT address

    LDR Rd, address
    STR Rd, address
    INP Rd, device
    OUT Rd, device

    MOV Rd, op2
    MVN Rd, op2

    ADD Rd, Rn, op2
    SUB Rd, Rn, op2
    AND Rd, Rn, op2
    ORR Rd, Rn, op2
    EOR Rd, Rn, op2
    LSL Rd, Rn, op2
    LSR Rd, Rn, op2

    CMP Rn, op2
    HALT


    # op__ c__s rn__ rd__  |  A?op eran d2__ ____
    # op__ c__s rn__ rd__  |  A?ad dres s___ ____
    

        MOV R0, #0
    loop:
        LDR R1, [R0]
        CMP R1, #0
        BEQ done
        OUT R1, DEV_CHAR
        ADD R0, R0, #1
        B loop

    done:
        HALT


    Immediate:
        "ADD R0, R0, #4"
        "LDR R0, 4"
    Indirect:
        "ADD R0, R0, R9"
        "LDR R0, [R1]"
