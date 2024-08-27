
import sys
import signal
import getpass

from pm import add_password, create_db, signal_handler, delete_all, remove_entry, get_mails, get_note, get_password, modify_entry, print_all, find_by_mail

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    create_db()
    print(" ╔═══════════════════════════════════╗ ")
    print(" ║    Password Manager by Stevees    ║ ")
    print(" ╚═══════════════════════════════════╝ ")
    try:
        while True:
            print()
            print()
            resp = input("What do you want to do?\n1- add new credentials\n2- search for an existing password\n3- modify a password\n4- delete a password\n5- view the entire database\n6- find all services linked to an account (email or username)\n7- delete the database\ni- info\nQ- quit\n\n---------------------------------------------------------\n")
            print("---------------------------------------------------------")

            if resp.lower() == 'q':
                sys.exit(0)
            
            elif resp == '1':
                print("Adding a new password")

                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    
                    master_password_confirmation = getpass.getpass(prompt="Re-enter the MASTER PASSWORD for confirmation: ")
                    if not master_password_confirmation:
                        print("The confirmation password cannot be empty. Please try again.")
                        continue
                    
                    if master_password != master_password_confirmation:
                        print("\nThe MASTER PASSWORDs do not match. Please try again.")
                    else:
                        break

                # master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                # master_password_confermation = getpass.getpass(prompt="Re-enter the MASTER PASSWORD for confirmation: ")


                # while master_password_confermation != master_password:
                #     print("\nThe MASTER PASSWORDs do not match.")
                #     master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                #     master_password_confermation = getpass.getpass(prompt="Re-enter the MASTER PASSWORD for confirmation: ")


                service_name = input("Enter the service name: ").lower().strip()
                while not service_name:
                    print("Service name cannot be empty.")
                    service_name = input("Enter the service name: ").lower().strip()

                email = input("Enter the email for the account: ").strip()
                while not email:
                    print("Email cannot be empty.")
                    email = input("Enter the email for the account: ").strip()

                password = input(f"Enter the password for the account '{email}': ").strip()
                while not password:
                    print("Password cannot be empty.")
                    password = input(f"Enter the password for the account '{email}': ").strip()
                note = input("Enter a NOTE (optional): ")
                print()
                add_password(service_name, email, password, note, master_password)
                print("---------------------------------------------------------")

            elif resp == '2':
                print("Searching for an existing password")
                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break
                service_name = input("Enter the service name: ").lower().strip()
                while not service_name:
                    print("Service name cannot be empty.")
                    service_name = input("Enter the service name: ").lower().strip()
                mails = get_mails(service_name)

                if not mails:
                    print("Service not found.")

                elif len(mails) == 1:
                    retrieved_mail = mails[0]
                    retrieved_password = get_password(service_name, retrieved_mail, master_password)
                    retrieved_note = get_note(service_name, retrieved_mail)[0]

                    if retrieved_password:
                        print(f"Password for account '{retrieved_mail}' of '{service_name}' is: {retrieved_password}")
                        if retrieved_note == "":
                            print("There are no notes")
                        else:
                            print(f"Notes for '{service_name}' are: {retrieved_note}")
                        print("---------------------------------------------------------")
                    else:
                        print("Incorrect MASTER PASSWORD or the entry does not exist.")
                else:
                    print(f"There are more account for the service '{service_name}'.")
                    print("Choose the one you want:")
                    for index, mail in enumerate(mails, start=1):
                        print(f"{index}. {mail}")

                    try:
                        choice = int(input("Insert corresponding number: "))
                        if 1 <= choice <= len(mails):
                            retrieved_mail = mails[choice - 1]
                            retrieved_password = get_password(service_name, retrieved_mail, master_password)
                            retrieved_note = get_note(service_name, retrieved_mail)[0]

                            if retrieved_password:
                                print(f"Password for account '{retrieved_mail}' of '{service_name}' is: {retrieved_password}")
                                if retrieved_note == "":
                                    print("There are no notes")
                                else:
                                    print(f"Notes for '{service_name}' are: {retrieved_note}")
                                print("---------------------------------------------------------")
                            else:
                                print("Incorrect MASTER PASSWORD or the entry does not exist.")
                        else:
                            print("Invalid choise.")
                    except ValueError:
                        print("Invalid choise. You have to insert a number.")

            elif resp == '3':
                print("Modifying password")
                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break

                old_service = input("Insert the service to modify: ").lower().strip()
                while not old_service:
                    print("Service name cannot be empty.")
                    old_service = input("Insert the service to modify: ").lower().strip()

                old_email = input("Insert the old account to modify: ").strip()
                while not old_email:
                    print("Email cannot be empty.")
                    old_email = input("Insert the old account to modify: ").strip()

                old_password = input("Insert the old password to modify: ").strip()
                while not old_password:
                    print("Password cannot be empty.")
                    old_password = input("Insert the old password to modify: ").strip()
                old_note = get_note(old_service, old_email)

                print()
                new_service = input("Insert the new service: ").lower().strip()
                while not new_service:
                    print("Service name cannot be empty.")
                    new_service = input("Insert the new service: ").lower().strip()

                new_email = input("Insert the new account: ").strip()
                while not new_email:
                    print("Email cannot be empty.")
                    new_email = input("Insert the new account: ").strip()

                new_password = input(f"Insert the new password for the account '{new_email}': ").strip()
                while not new_password:
                    print("Password cannot be empty.")
                    new_password = input(f"Insert the new password for the account '{new_email}': ").strip()

                new_note = input("Insert new notes (optional): ") or old_note

                modify_entry(old_service, old_email, old_password, new_service, new_email, new_password, new_note, master_password)
                print("---------------------------------------------------------")

            elif resp == '4':
                print("Deleting  a password")
                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break

                service_name = input("Insert the service: ").lower().strip()
                while not service_name:
                    print("Service name cannot be empty.")
                    service_name = input("Insert the service: ").lower().strip()

                email = input("Insert the account to delete: ").strip()
                while not email:
                    print("Email cannot be empty.")
                    email = input("Insert the account to delete: ").strip()

                password = input(f"Insert the password of account '{email}' for confirmation: ").strip()
                while not password:
                    print("Password cannot be empty.")
                    password = input(f"Insert the password of account '{email}' for confirmation: ").strip()


                safety = input(f"Are you sure you want to delete the password for the account '{email}'? This action cannot be undone. Digit Y to continue, any other key to cancel: ")
                if safety.lower() == 'y':
                    if get_password(service_name, email, master_password) == password:
                        ret = remove_entry(service_name, email, master_password)
                        if ret == 1:
                            print(f"Entry for service '{service_name}' and email '{email}' removed.")
                        elif ret == 2:
                            print("No enrty to remove found.")
                        elif ret == 0:
                            print(f"Error in decrtpting.")

                    else:
                        print("Wrong password. Cant't delete the entry.")
                print("---------------------------------------------------------")


            elif resp == '5':
                print("Viewing the entire database")
                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break
                result = print_all(master_password)
                for el in result:
                    print(f"Service: '{el[0]}', Email: '{el[1]}', Password: '{el[2]}', Note: {el[3]}")
                print("---------------------------------------------------------")  

            elif resp == '6':
                print("Finding all services linked to an account (email or username)")
                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break
                mail = input("Enter the email for the account: ").strip()
                while not mail:
                    print("Email cannot be empty.")
                    mail = input("Enter the email for the account: ").strip()

                result = find_by_mail(mail, master_password)
                for el in result:
                    print(f"Email: '{el[0]}', Service: '{el[1]}', Password: '{el[2]}', Note: {el[3]}")

                    
                



            elif resp == '7':
                print("Deleting the entire database")

                while True:
                    master_password = getpass.getpass(prompt="Enter the MASTER PASSWORD: ")
                    if not master_password:
                        print("The MASTER PASSWORD cannot be empty. Please try again.")
                        continue
                    else:
                        break

                print("ATTENTION! This operation can't be undone. All datas will be lost.")
                safety = input("Are you sure you want to delete the entire database? Digit Y to continue, any other key to cancel: ")
                if safety.lower() == 'y':
                    if delete_all(master_password) == 1:
                        print("All entry have been deleted.")
                    else:
                        print("MASTER PASSWORD wrong.")


                    

            elif resp.lower() == 'i':
                print("\nINFO")
                print("Choose the desired service by entering the corresponding number.")
                print("WARNING: You must use the same MASTER PASSWORD for both adding and retrieving a password, otherwise the service cannot be provided!")
                print("You will need to remember the MASTER PASSWORD, as it cannot be stored in the database.")
                print("In the email field, you can enter either the email address used for that account or a Username or UserID.")
                print("You can modify the service, email, password, and/or notes for each entry. The operation OVERWRITES the old data.")
                print("You can delete an entry by confirming the service, email, and password, losing the respective information PERMANENTLY.")

                print("---------------------------------------------------------\n")



            else:
                print("Insert a valid input: 1, 2, 3, 4, 5, 6, 7, i or Q.")

    except EOFError:
        signal_handler(signal.SIGINT, None)

