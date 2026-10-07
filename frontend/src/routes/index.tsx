import { Routes, Route } from "react-router-dom";
import { RootLayout } from "@/layouts/RootLayout";
import { HomePage } from "@/pages/HomePage";

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<RootLayout />}>
        <Route path="/" element={<HomePage />} />
      </Route>
    </Routes>
  );
}
