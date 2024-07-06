console.log("Hello World!!!!!");
var fun = function (name, age) {
    return "name ".concat(name, " age ").concat(age);
};
var filter = function (arr, pred) {
    var res = [];
    arr.forEach(function (item) {
        if (pred(item)) {
            res.push(item);
        }
    });
    return res;
};
var a = [1, 2, 3, 4, 5, 6, 7, 8, 9];
console.log(filter(a, function even(item) { return item % 2 === 0; }));
