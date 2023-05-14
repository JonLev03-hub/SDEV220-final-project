document.addEventListener("keypress", function (e) {
  if (e.keyCode === 13 || e.which === 13) {
    e.preventDefault();
    return false;
  }
});
document
  .getElementById("addItemButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();
    data_items = [
      "id",
      "name",
      "supplier_id",
      "price",
      "desc",
      "count",
      "category",
    ];

    let form = document.getElementById("addItemForm");
    let result = {};

    data_items.forEach((item) => {
      result[item] = form[item].value;
    });

    let res = await fetch("http://127.0.0.1:5000/api/item/add", {
      method: "POST",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    window.alert(json.msg);
    if (res.status == 200) {
      data_items.forEach((item) => {
        form[item].value = "";
      });
    }
  });

document
  .getElementById("searchButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("searchInput").value;
    let result = {
      id: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/items/${input}`, {
      method: "GET",
      //   body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);

    // edit the table data
    let table = document.getElementById("searchResults");
    table.innerHTML = "";
    json.forEach((item) => {
      table.innerHTML += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.count}</td><td>${item.category}</td></tr>`;
    });
  });

document
  .getElementById("deleteItem")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("deleteInput").value;
    let result = {
      id: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/item/delete`, {
      method: "DELETE",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);
    window.alert(json.msg);
  });

document
  .getElementById("sendChanges")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let result = {
      id: document.getElementById("changeInputId").value,
      subtract: document.getElementById("subtract").checked,
      quantity: document.getElementById("changeInputQuantity").value,
    };
    console.log(result);
    let res = await fetch(`http://127.0.0.1:5000/api/item/update`, {
      method: "PUT",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);
    window.alert(json.msg);
  });
