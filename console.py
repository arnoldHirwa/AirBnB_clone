#!/usr/bin/python3
"""The console of AirBNB"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import re
from shlex import split


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "Place",
        "State",
        "City",
        "Amenity",
        "Review"
    }

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """A command that exists the program\n"""
        return True

    def emptyline(self):
        """Prints an empty line"""
        pass

    def do_create(self, cls_name):
        """Creates a class instance"""
        cls_name = parse(cls_name)
        if len(cls_name) == 0:
            print("** class name missing **")
        elif cls_name[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            cls_name = cls_name[0]
            newItem = eval(cls_name)()
            storage.save()
            print(newItem.id)

    def do_count(self, cls):
        """Counts number of instances of a class"""
        cls = parse(cls)[0]
        all = storage.all()
        needed = [str(x) for x in all.values() if x.__class__.__name__ == cls]
        print(len(needed))

    def do_show(self, args):
        """Show the current value of a class instance"""
        array = parse(args)
        all = storage.all()
        length = len(array)
        if length == 0:
            print("** class name missing **")
        elif array[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif length == 1:
            print("** instance id missing **")
        elif not (f"{array[0]}.{array[1]}" in all.keys()):
            print("** no instance found **")
        else:
            print(all[f"{array[0]}.{array[1]}"])

    def do_destroy(self, args):
        """Destroys a class instance by id"""
        array = parse(args)
        length = len(array)
        all = storage.all()
        if length == 0:
            print("** class name missing **")
        elif array[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif length == 1:
            print("** instance id missing **")
        elif not (f"{array[0]}.{array[1]}" in all.keys()):
            print("** no instance found **")
        else:
            del all[f"{array[0]}.{array[1]}"]
            storage.save()

    def do_all(self, args):
        """Show all instances of class"""
        array = parse(args)
        length = len(array)
        all = storage.all()
        if length == 0:
            arr = []
            for v in all.values():
                arr.append(v.__str__())
            print(arr)
        elif array[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif length >= 1:
            needed = [str(x) for x in all.values()
                      if x.__class__.__name__ == array[0]]
            print(needed)

    def do_update(self, args):
        """Updates a class instance using cmd"""
        array = parse(args)
        length = len(array)
        all = storage.all()
        if length == 0:
            print("** class name missing **")
            return False
        elif array[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        elif length == 1:
            print("** instance id missing **")
            return False
        elif not (f"{array[0]}.{array[1]}" in all.keys()):
            print("** no instance found **")
            return False
        elif length == 2:
            print("** attribute name missing **")
            return False
        elif length == 3:
            try:
                type(eval(array[2])) == dict
            except Exception:
                print("** value missing **")
                return False

        if length == 4:
            obj = all[f"{array[0]}.{array[1]}"]
            if array[2] in obj.__class__.__dict__.keys():
                # get all atributes from child and parent class
                typ = type(obj.__class__.__dict__[array[2]])
                obj.__dict__[array[2]] = typ(array[3])
            else:
                obj.__dict__[array[2]] = array[3]
        elif length == 3 and type(eval(array[2]) is dict):
            for k, v in (eval(array[2])).items():
                obj = all[f"{array[0]}.{array[1]}"]
                if k in obj.__class__.__dict__.keys():
                    # to get atributes from child and parent class
                    typ = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = typ(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def default(self, args):
        """Default method for unhandled commands"""
        mapping = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        isArg = re.search(r"\.", args)
        if isArg:
            cls = args[:isArg.span()[0]]
            other = args[isArg.span()[1]:]
            if other and other != "":
                func = parse(other)[0]
                search = re.search(r"\((.*?)\)", other)
                spn = search.span()
                func = other[:spn[0]]
                arg = other[spn[0] + 1:spn[1] - 1]
                if func in mapping:
                    return mapping[func](cls + " " + arg)

        print(f"*** Unknown syntax: {args}")
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
