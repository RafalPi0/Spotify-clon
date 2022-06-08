(function () {
  const singleSong_playlist_btn = document.querySelector(
    ".singleSong_playlist-btn"
  );
  if (singleSong_playlist_btn) {
    target = document.querySelector(singleSong_playlist_btn.dataset.target);
    btn_close = document.querySelector(".modal .btn-close");

    const playlist_item = document.querySelectorAll(".modal .playlist-item-li");

    // Iterate over playlist_item
    playlist_item.forEach((element) =>
      // Add click event to every node
      element.addEventListener("click", () => {
        form_add_to_list = document.getElementById("form_add_to_list");
        list_title = document.querySelector("form.form #id_list_title");
        list_title.value = element.innerText;
        form_add_to_list.submit();
      })
    );

    if (target) {
      singleSong_playlist_btn.addEventListener(
        "click",
        function () {
          modifyModal(target);
        },
        false
      );
      btn_close.addEventListener(
        "click",
        function () {
          closeModal(target);
        },
        false
      );
    }
  }

  function modifyModal(target) {    
    target.classList.toggle("show");
    if (target.classList.contains("show")) {
      target.style.display = "block";
      open;
    } else {
      target.style.display = "none";
    }
  }
  function closeModal(target) {    
    target.classList.remove("show");
    target.style.display = "none";
  }
})();
