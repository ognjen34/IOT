import React, { useEffect, useState } from "react";
import DeviceCard from "../Components/DeviceCard";

function PI1() {
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
      }}
    >
      <DeviceCard
        label={"DHT - Room1"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=5`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
        graph2={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=6`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DHT - Room2"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=7`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
        graph2={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=8`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"PIR - Enterance"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=9`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"PIR - Room1"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=10`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"PIR - Room2"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=11`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DB - Enterance"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=4`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DUS - Enterance"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=12`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
      <DeviceCard
        label={"DUS - Enterance"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=13`}
            width="100%"
            height="200"
            frameBorder="0"
          ></iframe>
        }
      />
    </div>
  );
}

export default PI1;
