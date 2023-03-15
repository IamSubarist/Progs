let arrDay = []

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
today = dd + '/' + mm + '/' + yyyy;

arrDay.push(today)
let arrDayProof = arrDay.includes(today)

if (arrDayProof === true) {
    console.log('memoryplus');
} else {
    console.log('Перед началом работы нажмите кнопку "Сброс"')
}



window.currentUser = {
    name: "John"
  };
  
  // где угодно в коде
  alert(currentUser.name); // John