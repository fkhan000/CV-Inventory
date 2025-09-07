import "./navbar.css";
import { FaHome, FaTachometerAlt, FaUser } from "react-icons/fa";

export function Navbar({elements}) {

    const items = {
        "Home": {"link": "/", "icon": <FaHome />},
        "Dashboard": {"link": "/dashboard", icon: <FaTachometerAlt />},
        "Profile": {"profile": "/profile", icon: <FaUser />}
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