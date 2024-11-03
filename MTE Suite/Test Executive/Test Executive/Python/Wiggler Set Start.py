import deathstar_control
def main():
    dcon = deathstar_control.CDeathstarControl()
    dcon.Init()
    dcon.SetStartRelayON()
        
if __name__ == "__main__":
    main()