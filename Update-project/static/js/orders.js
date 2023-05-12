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
      if (item == "remove") {
        result[item] = form[item].checked;
        // console.log(form[item].checked);
      }
    });

    let ids = document.getElementsByClassName("orderItemId");
    let counts = document.getElementsByClassName("orderItemCount");
    console.log(ids);
    for (let i = 0; i < 5; i++) {
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
      table.innerHTML += `<tr><td>${item.orderId}</td><td>${item.customerId}</td><td>${item.date}</td><td>${item.price}</td></tr>`;
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
    let html = ` <div>Order Id: ${json.orderId}</div><div>Customer Id: ${json.customerId}</div><div>Order Date: ${json.date}</div><div>Order Price: ${json.price}</div><br><span>Items</span><table class = "dataTable"><thead><tr><td>Item Id</td><td>Item Count</td></tr></thead><tbody>`;
    for (item in json.items) {
      item = json.items[item];
      console.log(item);
      html += `<tr><td>${item.id}</td><td>${item.quantity}</td></tr>`;
    }
    html += "</tbody></table>  ";
    box.innerHTML = html;
    // json.forEach((item) => {
    //   table.innerHTML += ``;
    // });
  });
