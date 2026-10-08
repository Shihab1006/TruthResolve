import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

export function createReadClient() {
  return createClient({ chain: studionet });
}
