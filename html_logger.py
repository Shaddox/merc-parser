from datetime import datetime


def create_html_log(allNewProducts, path):
    html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               Here is all the new stuff you were curious about: <br>
            </p>
            <table>
            <tr>
                <th>Product Name</th>
                <th>Product Price</th>
                <th>Status</th>
                <th>Sold Out</th>
            </tr>
        """

    for newProduct in allNewProducts:
        html += f"""\
            <tr>
                <td><a href="{newProduct[2]}">{newProduct[1]}</a>
                <td>{newProduct[4]}</td>
                <td>{newProduct[5]}</td>
                <td>{newProduct[6]}</td>
            </tr>
            """

    html += """\
        </table>
        </body>
        </html>
        """

    # get current date and time
    x = datetime.now()

    filename = path + "Output " + x.strftime('%d-%m-%Y-%H-%M-%S.html')
    with open(filename, 'w', encoding="utf-8") as fp:
        print('created', filename)
        fp.write(html)
        fp.close()
