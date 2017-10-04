Format for command specifications:

- type: EXEC or SQL
  spec:
      components:
          - type: CONST or VAR
            value: string
            ioType: FILE or DIR (optional)
            asInput: bool (optional)
