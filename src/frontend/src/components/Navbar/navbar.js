import "./navbar.css";
import { FaHome, FaTachometerAlt, FaUser, FaSignInAlt, FaSign } from "react-icons/fa";

export function Navbar({elements}) {

    const items = {
        "Home": {"link": "/", "icon": <FaHome />},
        "Dashboard": {"link": "/dashboard", icon: <FaTachometerAlt />},
        "Profile": {"link": "/profile", icon: <FaUser />},
        "Login": {"link": "/login", icon: <FaSignInAlt/>}
    }
    return (
        <div className = "navbar">
            {elements.map( (el, i) => (
                <div className="item" key={i}>
                    {items[el].icon}
                    <a href={items[el].link}>{el}</a>
                </div>
            ))}
        </div>
    )
}