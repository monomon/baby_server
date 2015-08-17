var recordFields = [
	"id",
	"time",
	"kv",
	"bv",
	"poo",
	"pee",
	"temp",
	"weight",
	"vitaminD",
	"vitaminK",
	"kolikin",
	"notes"
];

function loadRecord(rowEl, fields)
{
	var form = document.querySelector("form");
	rowEl.addEventListener("click", function (evt) {
		// target is the cell clicked
		var cells = evt.target.parentNode.querySelectorAll("td");
		for (var j=0; j<recordFields.length; j++) {
			fields[j].value = cells.item(j).textContent;
		}
	});
}

document.addEventListener("DOMContentLoaded", function () {
	var form = document.querySelector("form");
	// cache list of input elements, ordered as in the name array
	var fieldEls = [];
	for (var i=0; i<recordFields.length; i++) {
		fieldEls.push(fields.getElementById(recordFields[i]));
	}
	var rows = document.querySelectorAll("tr");
	for (var i=0; i<rows.length; i++) {
		loadRecord(rows.item(i), fieldEls);
	}

	var cancelButton = document.querySelector("input.cancel[type=button]");
	cancelButton.addEventListener("click", function(evt) {
// + document.querySelectorAll("form textarea")
		for (var i=0; i<fieldEls.length; i++) {
			fieldEls[i].value = "";
		}
	});
});
