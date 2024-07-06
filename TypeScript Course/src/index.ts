class Person {
    public constructor(private _name: string, private _age: number) {}

    public get name() {
        return this._name;
    }

    public get age() {
        return this._age;
    }

    public set name(newName: string) {
        if (newName.length < 2) {
            throw new Error("Name can't be less than 2 characters");
        }
        this._name = newName;
    }

    public set age(newAge: number) {
        if (newAge < 0) {
            throw new Error("Age can't be negative");
        }
        if (newAge > 150) {
            throw new Error("Age can't be greater than 150");
        }
        this._age = newAge;
    }
}

let p = new Person("John", 20); 
console.log(p.name); // Correctly access the name property without parentheses

p.age = 30; // Correctly set the age
console.log(p.age); // Access the age property

p.name = "Jane"; // Correctly set the name
console.log(p.name); // Access the name property


