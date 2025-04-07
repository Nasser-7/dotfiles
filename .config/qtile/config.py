# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # --- ROOT ---
    # [ System ]
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # [ Layout ]
    Key([mod], "space", lazy.next_layout(), desc="Next layout"),
    Key([mod, "shift"], "space", lazy.prev_layout(), desc="Previous layout"),
    # [ Launcher ]
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc='Launch applications'),
    Key([alt], "tab", lazy.spawn("rofi -show window"), desc='See windows'),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take Screenshots"),
    #Key([mod], "r", lazy.spawncmd(),
    #    desc="Spawn a command using a prompt widget",
    #    ),

    # --- LAYOUTS ---
    # [ Navigation ]
    # Layouts: MonadTall, Max, TreeTab, Spiral & Floating.
    # MonadTall, ...
    Key([mod], "l", lazy.layout.right(), desc='Move focus to right'),
    Key([mod], "h", lazy.layout.left(), desc='Move focus to left'),
    # ...Max, TreeTab, Spiral ...
    Key([mod], "k", lazy.layout.up(), desc='Move focus up'),
    Key([mod], "j", lazy.layout.down(), desc='Move focus down'),
    # ...& Floating layout.
    Key([mod], "tab", lazy.group.prev_window(),
        # After switching focus bring the floating window to front.
        lazy.window.bring_to_front().when(when_floating=True),
        desc='Focus previous window',
        ),
    Key([mod, "shift"], "tab", lazy.group.next_window(),
        # After switching focus bring the floating window to front.
        lazy.window.bring_to_front().when(when_floating=True),
        desc='Focus next window',
        ),

    # [ Movement ]
    # MonadTall, ...
    Key([mod, "shift"], "l", lazy.layout.swap_right(),
        desc='Move window to the right',
        ),
    Key([mod, "shift"], "h", lazy.layout.swap_left(),
        desc='Move window to the left',
        ),
    # ...Spiral ... 
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), 
        # ...& Only TreeTab layout.
        lazy.layout.move_up().when(layout='treetab'),
        desc='Move window up',
        ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        # ...& Only TreeTab layout.
        lazy.layout.move_down().when(layout='treetab'),
        desc='Move window down',
        ),
    # [ Resizing ]
    # MonadTall ...
    Key([mod, "control"], "h", 
        lazy.layout.grow_main().when(layout='monadtall'),
        # ... & Spiral
        lazy.layout.grow_main().when(layout='spiral'),
        # ...& TreeTab Layout.
        lazy.layout.increase_ratio().when(layout='treetab'),
        desc="Grow window/Sidebar to the right",
        ),

    Key([mod, "control"], "l", 
        lazy.layout.shrink_main().when(layout='monadtall'),
        # ...& Spiral.
        lazy.layout.shrink_main().when(layout='spiral'),
        # ...& TreeTab Layout.
        lazy.layout.decrease_ratio().when(layout='treetab'), 
        desc="Grow window/Sidebar to the left",
        ),
    # MonadTall ...
    Key([mod, "control"], "k", lazy.layout.grow(),
        # ...& Spiral layout   
        lazy.layout.decrease_ratio().when(layout='spiral'), 
        desc="Grow window up",
        ),
    Key([mod, "control"], "j", lazy.layout.shrink(),
        # ...& Spiral layout
        lazy.layout.increase_ratio().when(layout='spiral'), 
        desc="Grow window down or 'increase ratio",
        ),
    # Monad Tall layout unique feature.
    Key([mod, "control"], "m", lazy.layout.toggle_auto_maximize(),
        desc = "Maximize Secondary windows",
        ),
    # Put all windows to his define values(E.g ratios).
    Key([mod, "control"], "r", lazy.layout.reset(), desc="Reset layout"),

    # --- WINDOWS ---
    # [ Properties ]
    Key([mod], "f", lazy.window.toggle_floating(), 
        desc="Toggle floating on the focused window",
        ),
    Key([mod], "m", lazy.window.toggle_maximize(), 
        desc="Toggle the maximize state of the window",
        ),
    Key([mod], "n", lazy.window.toggle_minimize(), lazy.layout.next(),
        desc="Toggle the minimize state of the window",
        ),
    Key([], "F11", lazy.window.toggle_fullscreen(),
        desc="Toggle the fullscreen state of the window",
        ),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    # [ Bonus ]
    Key([mod, "Control"], "n",
        lazy.group.unminimize_all(), lazy.group.next_window(), 
        desc="Unminize everything & get the focus",
        ),
    #Key([mod], "a", lazy.window.down_opacity(), 
    #desc="Down the opacity of the window 10%",
    #    ),
    #Key([mod], "a", lazy.window.up_opacity(),
    #desc="Up the opacity of the window 10%",
    #    ),
    #Key([mod, "control"], "c", lazy.window.center(),
    #    desc="Center the window",
    #    ),

    # --- GROUPS ---
    # [ Navigation ]
    # Vim keys 
    Key([alt], "l", lazy.screen.next_group(),
        desc="Move to the next group",
        ),
    Key([alt], "h", lazy.screen.prev_group(),
        desc="Move to the previous group",
        ), # Skipping groups without windows.
    Key([alt], "k", lazy.screen.next_group(skip_empty=True), 
        desc="Move to the next group available or with windows",
        ),
    Key([alt], "j", lazy.screen.prev_group(skip_empty=True), 
        desc="Move to the previous group available or with windows",
        ),
    # Arrows
    Key([mod], "right", lazy.screen.next_group(),
        desc="Move to the next group",
        ),
    Key([mod], "left", lazy.screen.prev_group(), 
        desc="Move to the previous group",
        ),
    # Skipping groups without windows.
    Key([mod], "up", lazy.screen.next_group(skip_empty=True), 
        desc="Move to the next group available",
        ),
    Key([mod], "down", lazy.screen.prev_group(skip_empty=True), 
        desc="Move to the previous group available",
        ),

    # [ Movement ]
    # Switch to a group 
    # TO DO LIST: DEFINE A FUNCTION TO DO MOVEMENT BETWEEN GROUPS VIA KEYBINDS
    # INSTEAD OF NAMES/NUMBERS.
    # Vim keys
    #Key([alt, "shift"], "l", lazy.function(toPrevGroup),
    #    desc="Switch to and move focus window to the next group",
    #    ),
    #Key([alt], "h", lazy.function(window_to_next_group),
    #    desc="Switch to and move focus window to the previous group"),
    #Key([alt, "shift"], "k", lazy.function(), 
    #    desc="Switch to and move focus window to the next group available"),
    #Key([alt, "shift"], "j", lazy.function(), 
    #    desc="Switch to and move focus window to the prev. group available"),
    # Arrows
    #Key([mod, "shift"], "right", lazy.function(window_to_next_group),
    #    desc="switch to and move focus window to the next group"),
    #Key([mod, "shift"], "left", lazy.function(window_to_prev_group), 
    #    desc="Switch to and move focus window to the previous group"),
    #Key([mod, "shift"], "up", lazy.function(), 
    #    desc="switch to and move focus window to the next group available"),
    #Key([mod, "shift"], "down", lazy.function(), 
    #    desc="Switch to and move focus window to the prev. group available"),
        ]

groups = [
    Group('1', label=''),
    Group('2', matches=[Match(role="browser")], layout = "max", label=''),
    Group('3', matches=[Match(wm_class="Mail")], layout = "max", label=''),
    Group('4', label=''),
    Group('5', label=''),
    Group('6', label=''),
    Group('7', matches=[Match(wm_class="discord")], label=''),
    Group('8', label=''),
          ]
for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key( [mod], i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key( [mod, "shift"], i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_focus": '89b482',
    "border_normal": 'd4be98',
    "border_width": 3,
    "margin": 5,
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        align = 1,
        auto_maximize = True,    # Maximize secondary windows automatically.
        change_ratio = 0.02,     # Value of changing ratio (Horizontally).
        change_size = 10,        # Value of changing size (Vertically).
        max_ratio = 0.54,         # Maximum value of ratio
        min_ratio = 0.46,        # Minimun value of ratio
        min_secondary_size = 58, # Minimun vertical size for secondary windows.
        ratio = 0.54,            # Default value of ratio.
        ),
    layout.Max(
        #margin = 5,
        **layout_theme,
        #only_focused = False, # idk what does this
        ),
    #layout.TreeTab(
    #    **layout_theme,
    #    ),
    #layout.Spiral(
    #    **layout_theme,
    #    ),
    layout.Floating(**layout_theme),
]

floating_layout = layout.Floating(**layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="pavucontrol"),
        Match(title="Brave"),
        Match(role="pop-up"),
        Match(wm_class="Tk"),
    ]
)


#   BBB  A  RR  SSS  
#   B B  A  R R S 
#   BBB A A RRR SSS     
#   B B AAA R R   S     
#   BBB A A R R SSS     

# Function to make the specified window name short
def windowName(text):
    for string in ["LibreWolf", "nvim", "Brave", "Discord", "Thunderbird", "Code"]:
        if string in text:
            text = string
        else:
            text = text
    return text
# Widget decorations settings
decor = {
    "decorations": [
        RectDecoration(
            colour = '1d2021',
            radius = 10,
            filled = True,
            group = True,
            padding_y = 5,

        ),
    ],
}
# Widget defaults settings
widget_defaults = dict(
        font = "Inter",
        fontsize = 14,
        padding = 10,
        background = '00000000', # TRANSPARENT
        foreground = 'ebdbb2',
        )   

extension_defaults = widget_defaults.copy()
# List of Widgets
left= [
        widget.Spacer(length = 5),
        widget.CurrentLayoutIcon(
            #custom_icon_paths=["~/.config/qtile/Assets/layouts/*.jpg *.svg"],
            scale = 0.60,
            **decor,
            ), 
        widget.Spacer(length = 10),

        widget.GroupBox(
            fontsize = 24,
            active = 'd4be98',  # Groups with windows. Soft White.
            inactive = '665c54', # Groups without windows. Grey.
            this_current_screen_border = '89b482',  # Groups focused. Blue.
            highlight_method = 'text',  # Highlight the text
            urgent_alert_method = 'text',
            urgent_text = 'ea6962',
            invert_mouse_wheel = True,
            disable_drag = True,
            padding = 0,
            margin_x = 5,
            **decor,
            ),
        widget.Spacer( length = 10),

        widget.TaskList(
            background = '00000000',    # The same as the bar
            stretch = False,
            icon_size = 0,
            parse_text = windowName,
            txt_floating = "  ",
            txt_maximized = "+",
            txt_minimized = "-",
            highlight_method = 'text',
            border = '89b482',
            urgent_alert_method = 'text',
            urgent_border = 'ea6962',
            padding = 7,
            **decor,
            ),
        widget.Spacer(length = 10),

        widget.CheckUpdates(
            distro='Arch_paru_Sup',
            initial_text='',
            display_format='󰚰',
            colour_have_updates='ea6962',
            execute = 'kitty -e paru',
            **decor,
            ),
        widget.Spacer(),
        ]

middle= [
        widget.Clock(
            #mouse_callbacks = {'Button1': lazy.spawn("calendar??")},
            format= "%A, %B %d of %Y. %H:%M:%S",
            **decor,
            ),
        ]

right= [
        widget.Spacer(),

        #widget.Mpd2(
        #    **decor,
        #    ),
        widget.StatusNotifier(
            **decor,
            ),
        widget.Spacer (length = 10),

        widget.ThermalSensor(
            format = '  {temp:.1f}{unit}',
            threshold = 69.1,
            foreground_alert = 'ea6962',
            update_interval = 1,
            **decor,
            ),
        widget.Spacer (length = 10),
        #widget.Memory(
        #    measure_mem = 'G',
        #    measure_swap = 'G',
        #    format = '  {MemUsed: .2f}{mm} /{MemTotal: .1f}{mm}',
        #    #format = '  {MemUsed: .2f}{mm} /{MemTotal: .1f}{mm} ({MemPercent: .0f}%)',
        #    **decor,
        #    ),
        #widget.Spacer (length = 10),

        widget.Volume(
            emoji=True,
            emoji_list=['','','',''],
            update_interval = 0.1,
            step = 1,
            volume_app='pavucontrol',
            padding = 6,
            **decor,
            ),
        widget.Volume(
            unmute_format = '{volume}%',
            mute_format = '{volume}%',
            update_interval = 0.1,
            step = 1,
            volume_app='pavucontrol',
            padding = 6,
            **decor,
            ),
        widget.Spacer( length = 10),

        #widget.Bluetooth(
        #    foreground = '7daea3',
        #    adapter_format = 'Adapter: {name} [{powered}{discovery}]',
        #    default_show_battery = True,
        #    default_text = '{connected_devices}',
        #    device_battery_format = ' ({battery}%)',
        #    device_format = 'Device: {name}{battery_level} [{symbol}]',
        #    **decor,
        #    ),
        #widget.Spacer(length = 10),

        widget.WiFiIcon(
            padding = 11,
            interface = 'wlp4s0',
            disconnected_colour = 'ea6962',
            inactive_colour = '928374',
            show_ssid = False,
            check_connection_interval = 1,
            #mouse_callbacks={Button2: lazy.function()}
            **decor,
            ),
        widget.Spacer(length = 10),

        widget.TextBox(
            fontsize = 21,
            fmt = "⏻",
            mouse_callbacks={
                'Button1': lazy.spawn(
                    "sh -c ~/.config/rofi/scripts/powermenu.sh")},
            **decor,
            ),
        widget.Spacer(length = 5),
        ]

# Define the widgets
# Define the bar in the screen with the widgets and the config bar too!!!
screens = [
    Screen(
        top = bar.Bar(
            left +  middle + right,
            backgroud = '#00000000',
            margin = [5, 5, 0, 5], #North, East, South, West. Clockwise.
            size = 36,
            ),
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", 
         lazy.window.set_position_floating(), start=lazy.window.get_position()
         ),
    Drag([mod], "Button3", 
         lazy.window.set_size_floating(), start=lazy.window.get_size()
         ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Autostart process like feh, notification daemon, ...
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])

# MISCELLANOUS
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = "Capitaine Cursors - White"
wl_xcursor_size = 34

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
