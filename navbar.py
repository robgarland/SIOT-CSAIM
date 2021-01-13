# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:47:39 2021

@author: garla
"""

import dash_bootstrap_components as dbc

def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("All Data", href="/all-data")),
              dbc.NavItem(dbc.NavLink("Aim Breakdown", href="/aim-breakdown"))
              # dbc.DropdownMenu(
              #    nav=True,
              #    in_navbar=True,
              #    label="Menu",
              #    children=[
              #       dbc.DropdownMenuItem("Aim Breakdown",href="/aim-breakdown"),
              #       dbc.DropdownMenuItem(divider=True),
              #       dbc.DropdownMenuItem("Insights",href="/insights"),
              #             ],
              #         ),
                    ],
          brand="CS:GO Aim Dashboard",
          brand_href="/dashboard",
          sticky="top",
        )
     return navbar