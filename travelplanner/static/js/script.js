function getOption() {
  var obj1 = document.getElementById("Line");
  var demo1 = obj1.options[obj1.selectedIndex].text;

  var obj2 = document.getElementById("Product");
  var demo2 = obj2.options[obj2.selectedIndex].text;

  var obj3 = document.getElementById("Part Number");
  var demo3 = obj3.options[obj3.selectedIndex].text;
}
