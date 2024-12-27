use rusty_engine::{game, prelude::*};
use rand::prelude::*;

#[derive(Resource)]
struct GameState {
    health_amount: u8,
    lost: bool,
}
impl Default for GameState {
    fn default() -> Self {
        Self {
            health_amount: INITIAL_HEALTH,
            lost: false,
        }
    }
}

const PLAYER_SPEED: f32 = 250.0;
const ROAD_SPEED: f32 = 400.0;
const INITIAL_HEALTH: u8 = 5;
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

    // add roadlines
    for i in 0..10 {
        let roadline = game.add_sprite(format!("roadline{}", i), SpritePreset::RacingBarrierWhite);
        roadline.scale = 0.1;
        roadline.translation.x = -600.0 + 150.0 * i as f32;
    }

    //add obstacles
    let obstacle_presets = vec![SpritePreset::RacingBarrelBlue,SpritePreset::RacingBarrelRed,SpritePreset::RacingConeStraight,SpritePreset::RacingBarrelBlue,SpritePreset::RacingBarrelRed,SpritePreset::RacingConeStraight];
    for (i,preset) in obstacle_presets.iter().enumerate(){
        let obstcle = game.add_sprite(format!("obstcle{}",i), *preset);
        obstcle.layer = 5.0;
        obstcle.collision = true;
        obstcle.translation.x = thread_rng().gen_range(800.0..1600.0);
        obstcle.translation.y = thread_rng().gen_range(-300.0..300.0);
    }

    // add health text
    let health_text = game.add_text("health_text", format!("Health: {}",INITIAL_HEALTH));
    health_text.translation = Vec2::new(550.0,320.0);
    
    game.add_logic(game_logic);
    game.run(GameState::default());
}

fn game_logic(engine: &mut Engine, game_state: &mut GameState) {
    if game_state.lost {
        return;
    }

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

    // move roadlines
    for sprite in engine.sprites.values_mut(){
        if sprite.label.starts_with("roadline"){
            sprite.translation.x -= ROAD_SPEED * engine.delta_f32;
            if sprite.translation.x < -675.0 {
                sprite.translation.x += 1500.0;
            }
        }

        if sprite.label.starts_with("obstcle"){
            sprite.translation.x -= ROAD_SPEED * engine.delta_f32;
            if sprite.translation.x < -800.0 {
                sprite.translation.x = thread_rng().gen_range(800.0..1600.0);
                sprite.translation.y = thread_rng().gen_range(-300.0..300.0);
            }
        }
    }
    let health_text = engine.texts.get_mut("health_text").unwrap();
    for event in engine.collision_events.drain(..){
        if !event.pair.either_contains("player1") || event.state.is_end(){
            continue;
        }
        if game_state.health_amount > 0 {
            game_state.health_amount -= 1;
            health_text.value = format!("Health: {}",game_state.health_amount);
            engine.audio_manager.play_sfx(SfxPreset::Impact3, 0.5);
        }
        if game_state.health_amount == 0 {
            break;
        }
    }
    if game_state.health_amount == 0 {
        game_state.lost = true;
        engine.audio_manager.play_sfx(SfxPreset::Jingle3, 0.5);
        engine.audio_manager.stop_music();
        let game_over_text = engine.add_text("game_over_text", "Game Over");
        game_over_text.font_size = 128.0;
    }
}
