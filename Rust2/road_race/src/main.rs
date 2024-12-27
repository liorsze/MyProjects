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
fn main() {
    let mut game = Game::new();

    // game setup goes here
    // add music
    game.audio_manager.play_music(MusicPreset::WhimsicalPopsicle, 0.2);

    // add player1 sprite
    let player1 = game.add_sprite("player1",SpritePreset::RacingCarBlue);
    player1.translation.x = -500.0;
    player1.layer = 10.0;
    player1.collision = true;

    game.add_logic(game_logic);
    game.run(GameState::default());
}

fn game_logic(engine: &mut Engine, game_state: &mut GameState) {
    // game logic goes here
}