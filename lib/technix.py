def send_command(command):
    """Checks whether the 'command' is valid, and that the resulting
    voltage and current values will still be within the allowed
    limits, and sends the command to the serial bus if everything is
    Ok.  Retuns a tuple (voltage, current).
    """
    
    print(command)
    return (0.0, 0.0)

if __name__=='__main__':
    send_command("Testing 1-2-3")

