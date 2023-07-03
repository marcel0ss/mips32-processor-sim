import logging
import os
import Procesor as proc

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    proc =  proc.Processor()
    proc.run()



# autopep8 --in-place --aggressive --aggressive <filename>
# python3.11 -m unittest tests/Test*.py
