document.addEventListener("keypress", function (e) {
  if (e.keyCode === 13 || e.which === 13) {
    e.preventDefault();
    return false;
  }
});
document
  .getElementById("addCustomerButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();
    data_items = ["id", "name", "phone", "email"];

    let form = document.getElementById("addCustomerForm");
    let result = {};

    data_items.forEach((item) => {
      result[item] = form[item].value;
    });

    let res = await fetch("http://127.0.0.1:5000/api/customer/add", {
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
    let res = await fetch(`http://127.0.0.1:5000/api/customers/${input}`, {
      method: "GET",
      //   body: JSON.stringify(result),
    });
    // console.log(input);
    let json = await res.json();
    console.log(json);

    // edit the table data
    let table = document.getElementById("searchResults");
    table.innerHTML = "";
    json.forEach((customer) => {
      table.innerHTML += `<tr><td>${customer.id}</td><td>${customer.name}</td><td>${customer.phone}</td><td>${customer.email}</td></tr>`;
    });
  });

document
  .getElementById("deleteCustomer")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("deleteInput").value;
    let result = {
      id: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/customer/delete`, {
      method: "DELETE",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);
    window.alert(json.msg);
  });
