import { Stack } from "expo-router";
import Navbar from "./Navbar";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        header: () => <Navbar />,
      }}
    />
  );
}