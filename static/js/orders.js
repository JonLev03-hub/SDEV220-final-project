document.addEventListener("keypress", function (e) {
  if (e.keyCode === 13 || e.which === 13) {
    e.preventDefault();
    return false;
  }
});
document
  .getElementById("addOrderButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();
    data_items = ["id", "customer", "remove"];

    let form = document.getElementById("addorderForm");
    let result = {
      items: [],
    };

    data_items.forEach((item) => {
      result[item] = form[item].value;
    });

    let ids = document.getElementsByClassName("orderItemId");
    let counts = document.getElementsByClassName("orderItemCount");
    console.log(ids);
    for (let i = 0; i < 5; i++) {
      if (ids[i].value == "") continue;
      result.items.push({ id: ids[i].value, count: counts[i].value });
    }

    console.log(result);
    let res = await fetch("http://127.0.0.1:5000/api/order/add", {
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
    let res = await fetch(`http://127.0.0.1:5000/api/orders/${input}`, {
      method: "GET",
      //   body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);

    // edit the table data
    let table = document.getElementById("searchResults");
    table.innerHTML = "";
    json.forEach((item) => {
      table.innerHTML += `<tr><td>${item.id}</td><td>${item.customer}</td><td>${item.date}</td></tr>`;
    });
  });

document
  .getElementById("deleteOrder")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("deleteInput").value;
    let result = {
      id: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/order/delete`, {
      method: "DELETE",
      body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);
    window.alert(json.msg);
  });

document
  .getElementById("getSingleOrderButton")
  .addEventListener("click", async (event) => {
    event.preventDefault();

    let input = document.getElementById("findSingleOrder").value;
    let result = {
      id: input,
    };
    let res = await fetch(`http://127.0.0.1:5000/api/order/${input}`, {
      method: "GET",
      //   body: JSON.stringify(result),
    });
    let json = await res.json();
    console.log(json);

    // edit the table data
    let box = document.getElementById("orderInfoBox");
    let html = ` <div>Order Id: ${json.orderId}</div><div>Customer Id: ${json.customerId}</div><div>Order Date: ${json.date}</div><span>Items</span><table class = "dataTable"><thead><tr><td>Item Id</td><td>Item Count</td></tr></thead><tbody>`;
    for (item in json.items) {
      item = json.items[item];
      console.log(item);
      html += `<tr><td>${item.id}</td><td>${item.count}</td></tr>`;
    }
    html += "</tbody></table>  ";
    box.innerHTML = html;
    // json.forEach((item) => {
    //   table.innerHTML += ``;
    // });
  });
