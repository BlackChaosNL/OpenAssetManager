import type { RouteSectionProps } from "@solidjs/router"

import { Menu } from "./Menu"


export const Layout = (props: RouteSectionProps) => {
  return (
    <div class="flex flex-row flex-wrap w-dvh">
        <div class="h-screen bg-amber-600  w-1/4 pl-10 pr-10 pt-8">
            <Menu />
        </div>
        <div class="h-screen pl-6 pt-8">
            {props.children}
        </div>
    </div>
  )
}
 