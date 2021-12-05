// This file is for the double click of the mouse function and assigning it to a dropdown menu
// for recommendations to misspelled or context sensitive words.

// Sets up and creates a double click function for the dropdown menu
$(document).ready(function () {
    var divArea = $("#InputOutputDiv");
    divArea.css({ cursor: 'pointer' });
    divArea.dblclick(function (event) {
        var selection = window.getSelection();
        var word = $.trim(selection.toString());
        console.log(word);
        // **********************
        // if word is a misspelled or context sensitive, then send to function:
        // recsMenu(word, event, recommendations);
        // NOTE: I'm not sure how to get the recommendations to this .js file
        // **********************
    });
});

// Get corrections and display in a dropdown menu
function recsMenu(word, event, recommendations) {
    docArea = "divArea"
    markedWord = '<span style="text-decoration: underline 2px red;">' + word + '</span>'
    menu = ".context-menu"
    menuItem = ".context-menu li"
    menuItemID = '#ItemList'
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
    },
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
    document.getElementById(docArea).innerHTML = document.getElementById(docArea).innerHTML.replace(markedWord, correct);
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
