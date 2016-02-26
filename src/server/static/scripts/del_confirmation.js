  window.onload = function() {
    document.getElementById("del_link").style.display = 'none';
  }

  var toggle = function() {
    var mydiv = document.getElementById('del_link');

    if (mydiv.style.display === 'block' || mydiv.style.display === '')
      mydiv.style.display = 'none';
    else
      mydiv.style.display = 'block';
  }
