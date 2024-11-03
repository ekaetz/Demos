import deathstar_control
def main():
    dcon = deathstar_control.CDeathstarControl()
    dcon.Init()
    ioState = dcon.ReadRunningState()
    print ioState

if __name__ == "__main__":
    main()