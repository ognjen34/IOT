import { React, useEffect ,useState} from "react";
import { Typography, Button } from "@mui/material";
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import IconButton from '@mui/icons-material/Circle';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import axios from "axios";

function BedroomRGB()
{
    const [bulbColor, setBulbColor] = useState("primary")

    const handleColorChange = (color) => {
        if (color === "off"){
            setBulbColor("primary")
        }
        else{
            setBulbColor(color);
        }
        let colorUpper = color.toUpperCase()
        axios.post("http://localhost:5000/brgb", {mode:colorUpper})
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error(error);
        });

    };

    return (
        <div>
            <LightbulbIcon
                sx={{color:bulbColor, fontSize:"50px"}}
            />
            <div style={{ display: "flex", flexDirection: "row", justifyContent:"center" }}>
                {["red", "green", "blue", "purple", "lightblue", "yellow"].map((color, index) => (
                    <Button onClick={() => handleColorChange(color)}>
                        <IconButton
                            key={index}
                            sx={{ color: color, fontSize:"40px", margin:"0px" }}
                            
                        />
                    </Button>
                ))}
                <Button onClick={() => handleColorChange("off")}>
                    <PowerSettingsNewIcon sx={{color:"black",fontSize:"40px"}}/>
                </Button>
            </div>
        </div>
    )
}

export default BedroomRGB;