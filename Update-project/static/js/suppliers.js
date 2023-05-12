document
  .getElementById("addSupplierButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();
    data_items = ["id", "name", "phone", "email"];

    let form = document.getElementById("addSupplierForm");
    let result = {};

    data_items.forEach((item) => {
      result[item] = form[item].value;
    });

    let res = await fetch("http://127.0.0.1:5000/api/supplier/add", {
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
    let res = await fetch(`http://127.0.0.1:5000/api/suppliers/${input}`, {
      method: "GET",
      //   body: JSON.stringify(result),
    });
    // console.log(input);
    let json = await res.json();
    console.log(json);

    // edit the table data
    let table = document.getElementById("searchResults");
    table.innerHTML = "";
    json.forEach((supplier) => {
      table.innerHTML += `<tr><td>${supplier.id}</td><td>${supplier.name}</td><td>${supplier.phone}</td><td>${supplier.email}</td></tr>`;
    });
  });

document
  .getElementById("deleteSupplier")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("deleteInput").value;
    let result = {
      phone: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/supplier/delete`, {
      method: "DELETE",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);
    window.alert(json.msg);
  });
