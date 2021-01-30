# AQA Assembly


```Python
import aqa32

aqa32.emulate('''
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
