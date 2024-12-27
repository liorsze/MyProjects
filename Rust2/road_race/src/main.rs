use rusty_engine::prelude::*;

#[derive(Resource)]
struct GameState {
    health_amount: u8,
    lost: bool,
}
impl Default for GameState {
    fn default() -> Self {
        Self {
            health_amount: 5,
            lost: false,
        }
    }
}

const PLAYER_SPEED: f32 = 250.0;
fn main() {
    let mut game = Game::new();

    // game setup goes here
    // add music
    game.audio_manager
        .play_music(MusicPreset::WhimsicalPopsicle, 0.2);

    // add player1 sprite
    let player1 = game.add_sprite("player1", SpritePreset::RacingCarBlue);
    player1.translation.x = -500.0;
    player1.layer = 10.0;
    player1.collision = true;

    game.add_logic(game_logic);
    game.run(GameState::default());
}

fn game_logic(engine: &mut Engine, game_state: &mut GameState) {
    let mut diraction: f32 = 0.0; // 1.0 is up, 0.0 is not moving, -1.0 is down

    // keyboard input
    if engine.keyboard_state.pressed(KeyCode::Up) {
        diraction += 1.0;
    }
    if engine.keyboard_state.pressed(KeyCode::Down) {
        diraction += -1.0;
    }

    // move player1
    let player1 = engine.sprites.get_mut("player1").unwrap();
    player1.translation.y += diraction * PLAYER_SPEED * engine.delta_f32;
    player1.rotation = diraction * 0.15;
    if player1.translation.y > 360.0 || player1.translation.y < -360.0 {
        game_state.health_amount = 0;
    }
}
