import binascii
import os
from flask import Flask, json, render_template, make_response
import requests
from functools import wraps, update_wrapper
from datetime import datetime
import shopify

app = Flask(__name__,
            static_url_path='/resources',
            static_folder='static',
            template_folder='templates')

shop_url = os.environ.get("SHOPIFY_URL", "")
api_version = os.environ.get("SHOPIFY_API", "")
session = shopify.Session(shop_url, api_version,
                          os.environ.get("SHOPIFY_KEY", ""))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@nocache
@app.route('/')
def home():
    return render_template("index.html")


@nocache
@app.route("/products")
def products():
    query = """
    {
        products(first: 6) {
            edges {
                node {
                    id
                    title
                    description
                    productType
                    priceRangeV2 {
                        maxVariantPrice {
                            amount,
                            currencyCode
                        },
                        minVariantPrice {
                            amount,
                            currencyCode
                        }
                    }
                    totalInventory
                    metafield(namespace: "custom", key: "short_description") {
                        value
                    }
                    images(first: 1) {
                        edges {
                            node {
                            src
                            }
                        }
                    }
                }
            }
        }
    }
    """
    shopify.ShopifyResource.activate_session(session)
    resp = shopify.GraphQL().execute(query)
    resp = json.loads(resp)
    print(resp)
    return resp


@nocache
@app.route('/product/<id>')
def product(id):
    query = """
    {
        product(id: "gid://shopify/Product/%s") {
            id
            title
            description
            productType
            variants(first: 10) {
            edges {
                node {
                    id
                    title
                    price
                    inventoryQuantity
                }
            }
            }
            metafield(namespace: "custom", key: "short_description") {
                value
            }
            images(first: 10) {
            edges {
                node {
                src
                }
            }
            }
        }
    }
    """ % id

    shopify.ShopifyResource.activate_session(session)
    resp = shopify.GraphQL().execute(query)
    resp = json.loads(resp)
    productinfo = resp["data"]["product"]
    variants = [item["node"]
                for item in productinfo["variants"]["edges"]]
    description = productinfo["description"]
    shortdescription = productinfo["metafield"]["value"]
    title = productinfo["title"]
    print(productinfo)
    images = [item["node"]
              for item in productinfo["images"]["edges"]]
    print(images)
    stock = str(variants[0]["inventoryQuantity"])
    price = f"${float(variants[0]['price']):.2f} CAD"
    return render_template("product.html", PRODUCT_ID=id, PRODUCT_DESCRIPTION=description, PRODUCT_TITLE=title, PRODUCT_STOCK=stock, PRODUCT_IMAGES=images, SHORT_DESCRIPTION=shortdescription, PRODUCT_PRICE=price)


@app.route('/teapot')
def iamateapot():
    return "<img src=\"https://raw.githubusercontent.com/hiroharu-kato/neural_renderer/master/examples/data/example1.gif\">", 418


app.run("0.0.0.0", "5500")
