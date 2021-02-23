import React,{useState, useEffect} from 'react'
import { commerce } from "./lib/commerce";
import {Products,Navbar, Cart,Checkout } from "./components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";



const App = () => {
    const [products,setProducts]= useState([]);
    const [cart, setCart] = useState({});
    const [order, setOrder] = useState({});
    const [errorMessage, setErrorMessage] = useState("");

    const fetchProducts= async () => {
        const {data}= await commerce.products.list();

        setProducts(data);
    }

    const fetchCart = async ()=> {
        const cart =await commerce.cart.retrieve();
        setCart(cart);
    }

    const handleAddToCart = async (prodId, quanitity)=> {
        const {cart}= await commerce.cart.add(prodId,quanitity);
        setCart(cart);
    }

    const handleUpdateCartQty = async (prodId, quantity)=>{
        const {cart} = await commerce.cart.update(prodId, {quantity} );
        setCart(cart);
    };

    const handleRemoveFromCart= async (prodId)=>{
        const {cart}= await commerce.cart.remove(prodId);
        setCart(cart);
    }

    const handleEmptyCart = async ()=>{
        const {cart} = await commerce.cart.enpty();
        setCart(cart);
    }

    const refreshcart = async ()=>{
        const newCart = await commerce.cart.refresh();

        setCart(newCart);
    }

    const handleCaptureCheckout = async (checkoutTokenId, newOrder) => {
        try{
            const incommingOrder= await commerce.checkout.capture(checkoutTokenId, newOrder);

            setOrder(incommingOrder);
            refreshcart();

        }catch(error){
            setErrorMessage(error.data.error.message);
        }
    }

    useEffect(()=> {
        fetchProducts();
        fetchCart();
    }, []);
    
    return (
        <Router>
            <div>
                <Navbar totalItems={cart.total_items} />
                <Switch>
                    <Route exact path="/" >
                        <Products products={products} onAddToCart={handleAddToCart} />
                    </Route>
                    <Route exact path="/cart" >
                        <Cart cart={cart} 
                            handleEmptyCart={handleEmptyCart}
                            handleRemoveFromCart={handleRemoveFromCart}
                            handleUpdateCartQty={handleUpdateCartQty}
                         />
                    </Route>
                    <Route exaxt path="/checkout" >
                        <Checkout cart={cart} order={order} onCaptureCheckout={handleCaptureCheckout} error={errorMessage} />
                    </Route>

                   
                </Switch>

            </div>
        </Router>
    )
}

export default App;
