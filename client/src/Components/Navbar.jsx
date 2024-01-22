import { React, useEffect, useState } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import { Chip } from "@mui/material";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import AdbIcon from "@mui/icons-material/Adb";
import { Link, useNavigate } from "react-router-dom";
import io from "socket.io-client";
import axios from "axios";

const pages = ["Pi1", "Pi2", "Pi3","Alarm"];
const settings = ["Profile", "Account", "Dashboard", "Logout"];

function ResponsiveAppBar() {
  useEffect(() => {
    const socket = io.connect("http://localhost:5000");
    

    socket.on("people", (data) => {
      console.log("Received message from server:", data);
      setPeople(data);
    });

    // socket.on("alarm", (data) => {
    //   console.log("Received message from server:", data);
    //   setPeople(data);
    // });

    return () => {
      socket.disconnect();
    };
  }, []);

  

  useEffect(() => {
    const socket = io.connect("http://localhost:5000");
    

    socket.on("alarm", (data) => {
      console.log("Received message from server:", data);
      setAlarm(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const [people, setPeople] = useState(0);
  const [alarm, setAlarm] = useState("blue");


  const handleOpenNavMenu = (event) => {};

  const handleCloseNavMenu = () => {};

  const alarmOff = () => 
  {
    axios
    .get("http://localhost:5000/alarmoff")
    .then((response) => {
      console.log("RADI");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  }


  return (
    <AppBar sx={{ position: "fixed" }}>
      <Container maxWidth="xl" sx={{ position: "relative" }}>
        <Toolbar disableGutters>
          <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: "block", md: "none" },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: "none", md: "flex" },
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {pages.map((page) => (
              <Link to={"/" + page} style={{ textDecoration: "None" }}>
                <Button
                  key={page}
                  onClick={handleCloseNavMenu}
                  sx={{
                    fontSize: "30px",
                    marginRight: "100px",
                    my: 2,
                    color: "white",
                    display: "block",
                  }}
                >
                  {page}
                </Button>
              </Link>
            ))}
            <Typography
              sx={{ position: "absolute", left: "0", fontSize: "24px" }}
            >
              People: {people}
              
            </Typography>
            <Chip
            onClick = {() => alarmOff()}
              label={"Alarm"}

              style={{ position: "absolute", fontSize: "24px",right: "0",padding :"0px",borderRadius : "30px", backgroundColor :alarm,color :"white", height:"40px", marginBottom:"5px"}}
            />
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default ResponsiveAppBar;
