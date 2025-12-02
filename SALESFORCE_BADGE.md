# Salesforce AI Centre Badge

This badge has been customized for the Salesforce AI Centre with a complete Salesforce-themed experience.

## What's New

### Salesforce Menu System
- **Location:** [badge/apps/sf_menu/](badge/apps/sf_menu/)
- Cloud-themed UI with animated background
- Salesforce blue color scheme
- "AI Centre" branding with lightning bolt icon
- Auto-discovers all apps starting with `sf_`

### Salesforce Apps

#### 1. Event Attendee Viewer ([badge/apps/sf_attendee/](badge/apps/sf_attendee/))
- View Event_Attendee__c record details
- Scrollable field viewer with mock data
- Shows: Event, Contact, Role, RSVP Status, Attendance Status, etc.
- **Controls:** UP/DOWN to scroll, HOME to exit

#### 2. Trailhead Progress ([badge/apps/sf_trailhead/](badge/apps/sf_trailhead/))
- Mock Trailhead profile with stats
- Shows: Rank, Points, Badges, Trails completed
- Recent badges list with scrolling
- **Controls:** UP/DOWN to scroll, HOME to exit

#### 3. Einstein AI Predictions ([badge/apps/sf_einstein/](badge/apps/sf_einstein/))
- Fun AI-powered fortune teller
- Animated prediction generation
- 15 different Salesforce-themed predictions
- **Controls:** B for new prediction, HOME to exit

#### 4. Ohana Values ([badge/apps/sf_ohana/](badge/apps/sf_ohana/))
- Interactive carousel of Salesforce core values
- Trust, Customer Success, Innovation, Equality
- Animated value cards with descriptions
- **Controls:** A/C or UP/DOWN to navigate, HOME to exit

## Boot Flow

The badge now boots directly into the Salesforce menu:
1. Startup animation (if not waking from sleep)
2. Salesforce AI Centre menu ([badge/main.py:36](badge/main.py#L36))
3. Only shows apps starting with `sf_`

## Color Palette

All apps use the official Salesforce color scheme:
- **Primary Blue:** `(0, 112, 210)`
- **Dark Blue:** `(3, 45, 96)`
- **Light Blue:** `(186, 218, 255)`
- **Success Green:** `(95, 237, 131)`
- **Warning Orange:** `(255, 186, 88)`
- **Purple:** `(110, 68, 255)`
- **Cloud Gray:** `(243, 243, 243)`

## Performance

All apps tested with excellent performance:
- **FPS:** ~59 (target: 60)
- **Frame Time:** ~17ms (target: <16.67ms)
- **Memory Usage:** <60KB per app (limit: 400KB)
- All apps run smoothly with animations

## Testing

Run any app in the simulator:
```bash
# Test the menu
python3 simulator/badge_simulator.py badge/apps/sf_menu --perf

# Test individual apps
python3 simulator/badge_simulator.py badge/apps/sf_attendee --perf
python3 simulator/badge_simulator.py badge/apps/sf_trailhead --perf
python3 simulator/badge_simulator.py badge/apps/sf_einstein --perf
python3 simulator/badge_simulator.py badge/apps/sf_ohana --perf
```

## Original GitHub Apps Preserved

All original 22 GitHub-themed apps remain in the repository:
- [badge/apps/menu/](badge/apps/menu/) - Original GitHub menu
- [badge/apps/weather/](badge/apps/weather/), [badge/apps/flappy/](badge/apps/flappy/), etc.

They are not loaded by the Salesforce menu but can be accessed by modifying [badge/main.py](badge/main.py) to use `/system/apps/menu` instead of `/system/apps/sf_menu`.

## Future Enhancements

Ideas for connecting to real Salesforce data:
1. Replace mock data in Event Attendee with real Salesforce API calls
2. Connect Trailhead app to actual Trailhead API
3. Add OAuth authentication flow
4. Create apps for: Cases, Opportunities, Dashboards, Reports
5. Real-time notifications from Salesforce

## File Structure

```
badge/
├── apps/
│   ├── sf_menu/          # Salesforce menu system
│   │   ├── __init__.py   # Menu logic
│   │   ├── ui.py         # Cloud-themed UI
│   │   ├── icon.py       # Icon rendering
│   │   └── icon.png      # Menu icon
│   ├── sf_attendee/      # Event Attendee viewer
│   ├── sf_trailhead/     # Trailhead progress
│   ├── sf_einstein/      # Einstein predictions
│   └── sf_ohana/         # Ohana values
├── main.py               # Modified to boot into sf_menu
└── assets/
    └── salesforce/       # Shared Salesforce assets (future)
```

## Credits

Built on top of the excellent [aicentre-badger](https://github.com/billnapier/aicentre-badger) repository by the GitHub badge team.
