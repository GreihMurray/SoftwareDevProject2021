// This file is for the double click of the mouse function and assigning it to a dropdown menu
// for recommendations to misspelled or context sensitive words.

var word;
var selection;
var recommends;

function setRecommendations(recs){
    recommends = recs;
}

// Sets up and creates a double click function for the dropdown menu
$(document).ready(function () {
    var divArea = $("#InputOutputDiv");
    divArea.css({ cursor: 'pointer' });
    divArea.dblclick(function (event) {
        selection = window.getSelection();
        console.log(selection);
        word = $.trim(selection.toString());
        console.log(word);
        recsMenu();
    });
});

// Get corrections and display in a dropdown menu
function recsMenu() {
    recommendations = recommends[word];
    docArea = "divArea";
    markedWord = '<span style="text-decoration: underline;">' + word + '</span>';
    menu = ".context-menu";
    menuItem = ".context-menu li";
    menuItemID = '#ItemList';
    console.log(word);
    console.log(recommendations);
    setMenuItems(menuItemID, recommendations);
    console.log(document.getElementById("contextMenu").innerHTML);
    showMenu(menu, event);

    // If a menu item is clicked
    $(menuItem).click(function () {
        replaceWord(docArea, markedWord, this);
        hideMenu(menu);
    });

    // If the document is clicked somewhere else
    $(document).bind("mousedown", function (event) {
        if (!$(event.target).parents(menu).length > 0) {
            hideMenu(menu);
        }
    });
}

function setMenuItems(menu, items) {
  var menuItems = ''
  for (var item in items) {
    var itemVal = items[item];
    menuItems += '<li data-action="' + itemVal + '">' + itemVal + '</li>';
  }
  $(menu).empty().append(menuItems);
}

function replaceWord(docArea, markedWord, item) {
    var correct = $(item).attr("data-action");
    document.getElementById(word).innerHTML = $(item).text();
    document.getElementById(word).className = '';
}

function showMenu(menu, event) {
  $(menu).finish().toggle(100).
    css({
      top: event.pageY + "px",
      left: event.pageX + "px"
    });
}

function hideMenu(menu) {
  $(menu).hide(100);
}
