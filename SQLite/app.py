#!/usr/bin/env python3
from database import *


def commands_list():
    print("""
Command list:
  show
  lookup
  schema
  add recors
  update
  delete
  delete table
  rename table
  add column
  delete column
  rename column""")


def app():
    try:
        for i in range(command_num):
            cmd = input("Enter your command below: \n>>>")

            if cmd.lower() == 'show':
                choice = input("Do you want to show (a)ll or (s)pecific records? (a/s)")
                if choice.lower() == 'a':
                    show_all()
                elif choice.lower() == 's':
                    optional = input("SELECT rowid, * FROM students ")
                    show_all(optional)
                else:
                    print("[!] Invalid choice")
            elif cmd.lower() == 'lookup':

                query = input("Write the query below. \n>>>")
                lookup(query)

            elif cmd.lower() == 'schema':
                schema()

            elif cmd.lower() == 'add record':
                choice = input("Do you want to add (s)ingle record ot (m)any records? s/m")
                if choice == 'm':
                    records = []
                    record_num - int(input("How many records do you want to add ?"))
                    for j in range(record_num):
                        print(f"Let's add the record number [j+1]")
                        records.append((input("First name: "), input("Last name: "), input("Students name: ")))
                    add_many(records)
                elif choice == 's':
                    add_single(input("First nameL"), input("Last name"), input("Students name"))
                else:
                    print("[!] Invalid choice")

            elif cmd.lower() == 'update':
                column_name = input("Column name: ")
                old_value = input("Old value :")
                value = input("New value: ")
                update(column_name, value, old_value)

            elif cmd.lower() == 'delete':
                column_name = input("Column name: ")
                value = input("Value: ")
                delete(column_name, value)

            elif cmd.lower() == 'delete table':
                table_name = input("Table name: ")
                delete_table(table_name)

            elif cmd.lower() == 'raname table':
                table_name = input("Table name: ")
                new_name = input("New name: ")
                alter_raname_column(column_name, new_name)

            elif cmd.lower() == 'add column':
                column_name = input('Column name: ')
                data_type = input('Data type: ')
                alter_add(column_name, data_type)

            elif cmd.lower() == 'delete column':
                column_name = input('Column name: ')
                alter_delete(column_name)

            elif cmd.lower() == 'rename column':
                column_name = input('Column name: ')
                new_name = input('New name: ')
                alter_rename(column_name, new_name)

            else:
                print("[!] Invalid command name: ")
                commands_list()
    except (KeyboardInterrupt, EOFError):
        print()
        exit()


if __name__ == "__main__":
    commands_list = int(input("How many commnad do you want to execute?\ncommmand number: "))
    commands_list()
    app()
