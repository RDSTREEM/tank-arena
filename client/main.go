package main

import (
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/vector"
)

const screenWidth int = 800
const screenHeight int = 600
const tankSpeed float64 = 4

type Game struct {
	tankX float64
	tankY float64
}

func (g *Game) Update() error {
	if ebiten.IsKeyPressed(ebiten.KeyW) {
		g.tankY -= tankSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyA) {
		g.tankX -= tankSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyS) {
		g.tankY += tankSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyD) {
		g.tankX += tankSpeed
	}

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill((color.RGBA{20, 20, 30, 255}))
	vector.DrawFilledRect(screen, float32(g.tankX), float32(g.tankY), 32, 32, color.RGBA{0, 200, 0, 255}, false)
	ebitenutil.DebugPrint(screen, "Move with W A S D")
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func main() {
	var game *Game = &Game{
		tankX: float64(screenWidth) / 2,
		tankY: float64(screenHeight) / 2,
	}

	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Tank Arena - Starter")

	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
