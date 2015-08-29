
var recordFields = [
	"id",
	"time",
	"kv",
	"bv",
	"poo",
	"pee",
	"temp",
	"weight",
	"notes",
	"kolikin",
	"vitaminD",
	"vitaminK"
];

fieldEls = [];

function loadRecord(rowEl, fields)
{
	var form = document.querySelector("form");
	rowEl.addEventListener("click", function (evt) {
		// target is the cell clicked
		clearForm();
		var cells = evt.target.parentNode.querySelectorAll("td");
		for (var j=0; j<recordFields.length; j++) {
			var cell = cells.item(j);
			if (fields[j].type == "checkbox") {
				if (cell.textContent == "1") {
					fields[j].checked = true;
				} else {
					fields[j].checked = false;
				}
			} else {
				fields[j].value = cell.textContent;
			}
		}
	});
}

function clearForm()
{
	for (var i=0; i<fieldEls.length; i++) {
		if (fieldEls[i].type == "checkbox") {
			console.log(fieldEls[i]);
			fieldEls[i].checked = false;
		} else {
			fieldEls[i].value = "";
		}
	}
}

document.addEventListener("DOMContentLoaded", function () {
	var form = document.querySelector("form");
	// cache list of input elements, ordered as in the name array
	for (var i=0; i<recordFields.length; i++) {
		fieldEls.push(document.getElementById(recordFields[i]));
	}
	var rows = document.querySelectorAll("tr");
	for (var i=0; i<rows.length; i++) {
		loadRecord(rows.item(i), fieldEls);
	}

	var cancelButton = document.querySelector("input.cancel[type=button]");
	cancelButton.addEventListener("click", function(evt) {
		clearForm();
	});

	var deleteButton = document.querySelector("input.delete[type=button]");
	deleteButton.addEventListener("click", function(evt) {
		if (window.confirm("Are you sure you want to delete this entry?")) {
			document.querySelector("input.action[type=hidden]").value = "delete";
			console.log(document.querySelector("input.action[type=hidden]"));
			form.submit();

		}
	});
});
