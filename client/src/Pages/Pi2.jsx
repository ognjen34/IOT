import React, { useEffect, useState } from "react";
import DeviceCard from "../Components/DeviceCard";
import LCD from "../Components/LCD";

function PI2() {
  const [fromTimestamp, setFromTimestamp] = useState(0);
  const [toTimestamp, setToTimestamp] = useState(0);

  useEffect(() => {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000); // Subtract 1 hour in milliseconds

    setFromTimestamp(oneHourAgo.getTime());
    setToTimestamp(now.getTime());
  }, []);

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        marginTop : "100px"

      }}
    >
      <DeviceCard
        label={"DHT - Garage"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=14`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
        graph2={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=15`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DHT - Room3"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=16`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
        graph2={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=17`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard label={"LCD - Garage"} graph={<LCD></LCD>} />
      <DeviceCard
        label={"DS - Garage"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=18`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DUS - Garage"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=19`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"GSG - Garage"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=28`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
        graph2={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=27`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"PIR - Room3"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=21`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"PIR - Garage"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=20`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
    </div>
  );
}

export default PI2;
