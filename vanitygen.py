from multiprocessing import Process, Value, cpu_count
from ctypes import c_bool
from iconsdk.wallet.wallet import KeyWallet
import time
import sys

start_time = time.time()
result = Value(c_bool, False)


def generate_wallet(result, pattern):
    try:
        if result.value:
            sys.exit()
        while not result.value:
            wallet = KeyWallet.create()
            address = wallet.get_address()
            private_key = wallet.get_private_key()
            if address.startswith("hx" + pattern):
                print("ran for:", round(time.time() - start_time, 2), "seconds")
                print("address:", address)
                print("private key:", private_key)
                result.value = True
    except KeyboardInterrupt:
        sys.exit()


def main():
    try:
        pattern = sys.argv[1].lower()
        int(pattern, 16)
        if len(pattern) > 40:
            sys.exit('Invalid input! Only letters a-f and numbers 0-9 are allowed. Maximum length is 40 characters.')
        processes = []
        cores = cpu_count()
        for x in range(0, cores):
            processes.append(Process(target=generate_wallet, args=(result, pattern,)))
        for x in processes:
            x.start()
    except ValueError:
        sys.exit('Invalid input! Only letters a-f and numbers 0-9 are allowed.')
    except IndexError:
        sys.exit('No pattern to look for.')
    except KeyboardInterrupt:
        x.terminate()
        sys.exit('Quitting.')


if __name__ == "__main__":
    main()
